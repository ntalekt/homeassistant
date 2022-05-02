"""ESXi commands for ESXi Stats component."""

import logging
from pyVim.connect import SmartConnect, SmartConnectNoSSL
from pyVmomi import vim, vmodl  # pylint: disable=no-name-in-module

from .const import SUPPORTED_PRODUCTS

_LOGGER = logging.getLogger(__name__)


def esx_connect(host, user, pwd, port, ssl):
    """Establish connection with host/vcenter."""
    si = None

    # connect depending on SSL_VERIFY setting
    if ssl is False:
        si = SmartConnectNoSSL(host=host, user=user, pwd=pwd, port=port)
        current_session = si.content.sessionManager.currentSession.key
        _LOGGER.debug("Logged in - session %s", current_session)
    else:
        si = SmartConnect(host=host, user=user, pwd=pwd, port=port)
        current_session = si.content.sessionManager.currentSession.key
        _LOGGER.debug("Logged in - session %s", current_session)

    return si


def esx_disconnect(conn):
    """Kill connection from host/vcenter."""
    current_session = conn.content.sessionManager.currentSession.key
    try:
        conn._stub.pool[0][0].sock.shutdown(2)
        _LOGGER.debug("Logged out - session %s", current_session)
    except Exception as e:
        _LOGGER.debug(e)


def check_license(lic):
    """Retreieve license from connected system."""
    _LOGGER.debug("Checking license type")
    for lic in lic.licenses:
        for key in lic.properties:
            if key.key != "ProductName":
                continue
            elif key.key == "ProductName" and key.value not in SUPPORTED_PRODUCTS:
                continue
            elif key.key == "ProductName" and key.value == SUPPORTED_PRODUCTS[1]:
                _LOGGER.debug("Found %s license", key.value)
                return True
            elif key.key == "ProductName" and key.value == SUPPORTED_PRODUCTS[0]:
                _LOGGER.debug("Found %s license", key.value)
                for feature in lic.properties:
                    if feature.key == "feature":
                        if feature.value.key == "vimapi":
                            _LOGGER.debug("vSphere API feature enabled")
                            return True


def get_license_info(lic, host):
    """Get license information."""
    expiration = "n/a"
    product = "n/a"
    status = "n/a"

    for key in lic.properties:
        if key.key == "ProductName":
            product = key.value
        if key.key == "count_disabled":
            expiration = "never"
        if key.key == "expirationHours":
            expiration = round((key.value / 24))

    if isinstance(expiration, int):
        if expiration > 30:
            status = "Ok"
        if expiration <= 30:
            status = "Expiring Soon"
        if expiration < 1:
            status = "expired"
    else:
        status = "Ok"

    license_data = {
        "name": lic.name,
        "status": status,
        "product": product,
        "expiration_days": expiration,
        "host": host
    }

    _LOGGER.debug(license_data)

    return license_data


def get_host_info(host):
    """Get host information."""
    host_summary = host.summary
    host_state = host_summary.runtime.powerState
    host_name = host_summary.config.name.replace(" ", "_").lower()

    _LOGGER.debug("vmhost: %s state is %s", host_name, host_state)

    if hasattr(host_summary.runtime, 'inMaintenanceMode'):
        host_mm_mode = host_summary.runtime.inMaintenanceMode
    else:
        host_mm_mode = "N/A"

    if host_state == "poweredOn":
        host_version = host_summary.config.product.version
        host_build = host_summary.config.product.build
        host_uptime = round(host_summary.quickStats.uptime / 3600, 1)
        host_cpu_total = round(
            host_summary.hardware.cpuMhz * host_summary.hardware.numCpuCores / 1000, 1
        )
        host_mem_total = round(host_summary.hardware.memorySize / 1073741824, 2)
        host_cpu_usage = round(host_summary.quickStats.overallCpuUsage / 1000, 1)
        host_mem_usage = round(host_summary.quickStats.overallMemoryUsage / 1024, 2)
        host_vms = len(host.vm)
    else:
        host_version = "n/a"
        host_build = "n/a"
        host_uptime = "n/a"
        host_cpu_total = "n/a"
        host_cpu_usage = "n/a"
        host_mem_total = "n/a"
        host_mem_usage = "n/a"
        host_vms = "n/a"

        _LOGGER.debug("Unable to return stats for %s", host_name)

    host_data = {
        "name": host_name,
        "state": host_state,
        "version": host_version,
        "build": host_build,
        "uptime_hours": host_uptime,
        "cputotal_ghz": host_cpu_total,
        "cpuusage_ghz": host_cpu_usage,
        "memtotal_gb": host_mem_total,
        "memusage_gb": host_mem_usage,
        "maintenance_mode": host_mm_mode,
        "vms": host_vms,
    }

    _LOGGER.debug(host_data)

    return host_data


def get_datastore_info(ds):
    """Get datastore information."""
    ds_summary = ds.summary
    ds_name = ds_summary.name.replace(" ", "_").lower()
    ds_capacity = round(ds_summary.capacity / 1073741824, 2)
    ds_freespace = round(ds_summary.freeSpace / 1073741824, 2)
    ds_type = ds_summary.type.lower()

    ds_data = {
        "name": ds_name,
        "type": ds_type,
        "free_space_gb": ds_freespace,
        "total_space_gb": ds_capacity,
        "connected_hosts": len(ds.host),
        "virtual_machines": len(ds.vm),
    }

    _LOGGER.debug(ds_data)

    return ds_data


def get_vm_info(vm):
    """Get VM information."""
    vm_conf = vm.configStatus
    vm_sum = vm.summary
    vm_run = vm.runtime
    vm_snap = vm.snapshot

    vm_name = vm_sum.config.name.replace(" ", "_").lower()

    # If a VM configuration is in INVALID state, return Inalid status
    if vm_conf == "red":
        vm_data = {
            "name": vm_name,
            "status": "Invalid"
        }
        _LOGGER.debug(vm_data)
        return vm_data

    vm_tools_status = vm_sum.guest.toolsStatus
    vm_used_space = round(vm_sum.storage.committed / 1073741824, 2)

    # if snapshots present, get number of snapshots
    if vm_snap is not None:
        vm_snapshots = len(listSnapshots(vm_snap.rootSnapshotList))
    else:
        vm_snapshots = 0

    # set vm_state based on power state
    if vm_sum.runtime.powerState == "poweredOn":
        vm_state = "running"
    elif vm_sum.runtime.powerState == "poweredOff":
        vm_state = "off"
    elif vm_sum.runtime.powerState == "suspended":
        vm_state = "suspended"
    else:
        vm_state = vm_sum.runtime.powerState

    # set runtime related attributes based on vm power state
    if vm_state == "running":

        # check if stats exist and set values, otherwise return "n/a"
        if vm_sum.quickStats.overallCpuUsage and vm_run.maxCpuUsage:
            vm_cpu_usage = round(
                ((vm_sum.quickStats.overallCpuUsage / vm_run.maxCpuUsage) * 100), 2
            )
        else:
            vm_cpu_usage = "n/a"
            _LOGGER.debug("Unable to return cpu usage for %s", vm_name)

        if vm_sum.quickStats.hostMemoryUsage:
            vm_mem_usage = round(vm_sum.quickStats.hostMemoryUsage, 2)
        else:
            vm_mem_usage = "n/a"
            _LOGGER.debug("Unable to return memory usage for %s", vm_name)

        if vm_sum.quickStats.uptimeSeconds:
            vm_uptime = round(vm_sum.quickStats.uptimeSeconds / 3600, 1)
        else:
            vm_uptime = "n/a"
            _LOGGER.debug("Unable to return uptime for %s", vm_name)

        if vm_sum.guest.ipAddress:
            vm_ip = vm_sum.guest.ipAddress
        else:
            vm_ip = "n/a"
            _LOGGER.debug("Unable to return VM IP address for %s", vm_name)

        if vm_sum.guest.guestFullName:
            vm_guest_os = vm_sum.guest.guestFullName
        else:
            _LOGGER.debug(
                ("Unable to return Guest OS Name, using Configured Guest Name instead")
            )
            vm_guest_os = vm_sum.config.guestFullName
    else:
        vm_cpu_usage = "n/a"
        vm_mem_usage = "n/a"
        vm_ip = "n/a"
        vm_uptime = "n/a"
        vm_guest_os = vm_sum.config.guestFullName

    vm_data = {
        "name": vm_name,
        "status": vm_sum.overallStatus,
        "state": vm_state,
        "uptime_hours": vm_uptime,
        "cpu_count": vm_sum.config.numCpu,
        "cpu_use_pct": vm_cpu_usage,
        "memory_allocated_mb": vm_sum.config.memorySizeMB,
        "memory_used_mb": vm_mem_usage,
        "used_space_gb": vm_used_space,
        "tools_status": vm_tools_status,
        "guest_os": vm_guest_os,
        "guest_ip": vm_ip,
        "snapshots": vm_snapshots,
    }

    _LOGGER.debug(vm_data)

    return vm_data


def listSnapshots(snapshots, tree=False):
    """Get VM snapshot information.

    tree=True will return snapshot tree details required for snapshot removal
    """
    snapshot_data = []

    for snapshot in snapshots:
        if tree is True:
            snapshot_data.append(snapshot)
        else:
            snapshot_data.append(snapshot.id)
        snapshot_data = snapshot_data + listSnapshots(snapshot.childSnapshotList, tree)

    return snapshot_data


def vm_pwr(hass, target_host, target_vm, target_cmnd, conn_details):
    """VM power commands."""
    conn = esx_connect(**conn_details)
    content = conn.RetrieveContent()
    objView = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    data = objView.view
    objView.Destroy()

    try:
        for vm in [vm for vm in data if vm.name in target_vm]:
            _LOGGER.info("Sending '%s' command to vm '%s'", target_cmnd, vm.name)

            # generate task based on requested command
            if target_cmnd == "on":
                task = vm.PowerOnVM_Task()
            elif target_cmnd == "off":
                task = vm.PowerOffVM_Task()
            elif target_cmnd == "suspend":
                task = vm.SuspendVM_Task()
            elif target_cmnd == "reset":
                task = vm.ResetVM_Task()
            elif target_cmnd == "reboot":
                task = vm.RebootGuest()
            elif target_cmnd == "shutdown":
                task = vm.ShutdownGuest()

            # while task is running, check status
            # some tasks are fire and forget, no status will be provided
            if task:
                message = "power " + target_cmnd + " on " + vm.name
                taskStatus(hass, task, message)
            else:
                _LOGGER.info("'%s' task does not provide feedback", target_cmnd)

            break
        else:
            _LOGGER.info(
                "VM %s on host %s not found. Make sure the name is correct",
                target_vm,
                target_host,
            )
    except vmodl.MethodFault as e:
        _LOGGER.info(e.msg)
    except Exception as e:
        _LOGGER.info(str(e))
    finally:
        esx_disconnect(conn)

    return True


def vm_snap_take(
    hass, target_host, target_vm, snap_name, desc, memory, quiesce, conn_details
):
    """Take Snapshot commands."""
    conn = esx_connect(**conn_details)
    content = conn.RetrieveContent()
    objView = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    data = objView.view
    objView.Destroy()

    try:
        for vm in [vm for vm in data if vm.name in target_vm]:
            _LOGGER.info("Sending create snapshot command to vm '%s'", vm.name)
            task = vm.CreateSnapshot_Task(snap_name, desc, memory, quiesce)

            # while task is running, check status
            if task:
                message = "create snapshot on " + vm.name
                taskStatus(hass, task, message)
            else:
                _LOGGER.info("Task does not provide feedback")

            break
        else:
            _LOGGER.info(
                "VM %s on host %s not found. Make sure the name is correct",
                target_vm,
                target_host,
            )
    except vmodl.MethodFault as e:
        _LOGGER.info(e.msg)
    except Exception as e:
        _LOGGER.info(str(e))
    finally:
        esx_disconnect(conn)

    return True


def vm_snap_remove(hass, target_host, target_vm, target_cmnd, conn_details):
    """Remove Snapshot commands."""
    conn = esx_connect(**conn_details)
    content = conn.RetrieveContent()
    objView = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    data = objView.view
    objView.Destroy()

    try:
        for vm in [vm for vm in data if vm.name in target_vm]:
            # if there are 0 snapshots, stop
            if vm.snapshot is None:
                _LOGGER.info("No snapshots to remove on %s", vm.name)
                break

            _LOGGER.info(
                "Sending remove '%s' snapshot command to vm '%s'", target_cmnd, vm.name
            )

            # get a list of all snapshots
            snapshots = listSnapshots(vm.snapshot.rootSnapshotList, True)

            # remove all snapshots
            if target_cmnd == "all":
                task = vm.RemoveAllSnapshots_Task()
            # remove first snapshot in a snapshot tree
            elif target_cmnd == "first":
                first_snap = snapshots[0].snapshot
                task = first_snap.RemoveSnapshot_Task(False)
            # remove last snapshot in a snapshot tree
            elif target_cmnd == "last":
                last_snap = snapshots[(len(snapshots) - 1)].snapshot
                task = last_snap.RemoveSnapshot_Task(False)

            # while task is running, check status
            if task:
                message = "remove " + target_cmnd + " snapshot(s) on " + vm.name
                taskStatus(hass, task, message)
            else:
                _LOGGER.info("Task does not provide feedback")

            break
        else:
            _LOGGER.info(
                "VM %s on host %s not found. Make sure the name is correct",
                target_vm,
                target_host,
            )
    except vmodl.MethodFault as e:
        _LOGGER.info(e.msg)
    except Exception as e:
        _LOGGER.info(str(e))
    finally:
        esx_disconnect(conn)

    return True


def taskStatus(hass, task, command):
    """Check status of running task."""
    from time import sleep
    from homeassistant.components import persistent_notification

    # wait while task is in progress
    state = vim.TaskInfo.State
    while task.info.state not in [state.success, state.error]:
        if task.info.progress is not None:
            _LOGGER.debug(
                "Task %s progress %s", task.info.eventChainId, task.info.progress
            )

        sleep(2)

    # output task status once complete
    if task.info.state == "success":
        _LOGGER.info("Sending command to '%s' complete", task.info.entityName)

        message = "Complete - " + command
        persistent_notification.create(hass, message, "ESXi Stats")
    if task.info.state == "error":
        _LOGGER.info("Sending command to '%s' failed", task.info.entityName)
        _LOGGER.info(task.info.error.msg)

        message = "Failed - " + command + "\n\n"
        message += task.info.error.msg
        persistent_notification.create(hass, message, "ESXi Stats")
