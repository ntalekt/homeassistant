"""Definition of all the attributes per OBJTYP."""

NULL_OBJNAM = "00000"

BODY_TYPE = "BODY"
CHEM_TYPE = "CHEM"
CIRCUIT_TYPE = "CIRCUIT"
CIRCGRP_TYPE = "CIRCGRP"
HEATER_TYPE = "HEATER"
PMPCIRC_TYPE = "PMPCIRC"
PUMP_TYPE = "PUMP"
REMBTN_TYPE = "REMBTN"
REMOTE_TYPE = "REMOTE"
SCHED_TYPE = "SCHED"
SENSE_TYPE = "SENSE"
SYSTEM_TYPE = "SYSTEM"

ACT_ATTR = "ACT"
BODY_ATTR = "BODY"
CIRCUIT_ATTR = "CIRCUIT"
COMUART_ATTR = "COMUART"
DLY_ATTR = "DLY"
ENABLE_ATTR = "ENABLE"
FEATR_ATTR = "FEATR"
GPM_ATTR = "GPM"
HEATER_ATTR = "HEATER"
HNAME_ATTR = "HNAME"
HTMODE_ATTR = "HTMODE"
LISTORD_ATTR = "LISTORD"
LOTMP_ATTR = "LOTMP"
LSTTMP_ATTR = "LSTTMP"
MODE_ATTR = "MODE"
NORMAL_ATTR = "NORMAL"
OBJTYP_ATTR = "OBJTYP"
ORPTNK_ATTR = "ORPTNK"
ORPVAL_ATTR = "ORPVAL"
PARENT_ATTR = "PARENT"
PHVAL_ATTR = "PHVAL"
PHTNK_ATTR = "PHTNK"
PRIM_ATTR = "PRIM"
PROPNAME_ATTR = "PROPNAME"
PWR_ATTR = "PWR"
QUALTY_ATTR = "QUALTY"
READY_ATTR = "READY"
RPM_ATTR = "RPM"
SALT_ATTR = "SALT"
SELECT_ATTR = "SELECT"
SHOMNU_ATTR = "SHOMNU"
SNAME_ATTR = "SNAME"
SOURCE_ATTR = "SOURCE"
STATIC_ATTR = "STATIC"
STATUS_ATTR = "STATUS"
SUBTYP_ATTR = "SUBTYP"
SUPER_ATTR = "SUPER"
TIME_ATTR = "TIME"
TIMOUT_ATTR = "TIMOUT"
USE_ATTR = "USE"
VACFLO_ATTR = "VACFLO"
VER_ATTR = "VER"
VOL_ATTR = "VOL"

USER_PRIVILEGES = {
    "p": "Pool Access",
    "P": "Pool temperature",
    "h": "Pool Heat Mode",
    "m": "Spa Access",
    "S": "Spa Temperature",
    "n": "Spa Heat Mode",
    "e": "Schedule Access",
    "v": "Vacation Mode",
    "f": "Features Access",
    "l": "Lights Access",
    "c": "Chemistry Access",
    "u": "Usage Access",
    "C": "System Configuration",
    "o": "Support",
    "q": "Alerts and Notifications",
    "i": "User Portal",
    "k": "Groups",
    "a": "Advanced Settings",
    "t": "Status",
    "x": "Service Mode Circuits",
    "g": "General Settings",
}

# represents a body of water (pool or spa)
BODY_ATTRIBUTES = {
    "ACT1",  # (int) ???
    "ACT2",  # (int) ???
    "ACT3",  # (int) ???
    "ACT4",  # (int) ???
    "FILTER",  # (objnam) Circuit object that filter this body
    HEATER_ATTR,  # (objnam)
    "HITMP",  # (int) maximum temperature to set
    HNAME_ATTR,  # equals to OBJNAM
    HTMODE_ATTR,  # (int) >0 if currently heating, 0 if not
    "HTSRC",  # (objnam) the heating source (or '00000')
    LISTORD_ATTR,  # (int) used to order in UI
    LOTMP_ATTR,  # (int) desired temperature
    LSTTMP_ATTR,  # (int) last recorded temperature
    "MANHT",  # Manual heating ???
    "MANUAL",  # (int) ???
    PARENT_ATTR,  # (objnam) parent object
    "PRIM",  # (int) ???
    READY_ATTR,  # (ON/OFF) ???
    "SEC",  # (int) ???
    "SETPT",  # (int) set point (same as 'LOTMP' AFAIK)
    "SHARE",  # (objnam) sharing with that other body?
    SNAME_ATTR,  # (str) friendly name
    "SRCTYP",  # ??? only seeing "GENERIC"
    STATIC_ATTR,  # (ON/OFF) 'OFF'
    STATUS_ATTR,  # (ON/OFF) 'ON' is body is "active"
    SUBTYP_ATTR,  # 'POOL' or 'SPA'
    VOL_ATTR,  # (int) Volume in Gallons
}


CHEM_ATTRIBUTES = {
    "ALK",  # (int) IntelliChem: Alkalinity setting
    BODY_ATTR,  # (objnam) BODY being managed
    "CALC",  # (int) IntelliChem: Calcium Harness setting
    "CHLOR",  # (ON/OFF) IntelliChem: ??
    COMUART_ATTR,  # (int) X25 related ?
    "CYACID",  # (int) IntelliChem: Cyanuric Acid setting
    LISTORD_ATTR,  # (int) used to order in UI
    "ORPHI",  # (ON/OFF) IntelliChem: ORP Level too high?
    "ORPLO",  # (ON/OFF) IntelliChem: ORP Level too low?
    "ORPSET",  # (int) IntelliChem ORP level setting
    ORPTNK_ATTR,  # (int) IntelliChem: ORP Tank Level
    ORPVAL_ATTR,  # (int) IntelliChem: ORP Level
    "PHHI",  # (ON/OFF) IntelliChem: Ph Level too low?
    "PHLO",  # (ON/OFF) IntelliChem: Ph Level too low?
    "PHSET",  # (float) IntelliChem Ph level setting
    PHTNK_ATTR,  # (int) IntelliChem: Ph Tank Level
    PHVAL_ATTR,  # (float) IntelliChem: Ph Level
    PRIM_ATTR,  # (int) Intellichor: output setting in %
    QUALTY_ATTR,  # (float) Intellichem: Water Quality (Saturation Index)
    SALT_ATTR,  # (int) Salt level
    "SEC",  # (int) IntelliChlor ??
    "SHARE",  # (objnam) ??
    "SINDEX",  # (int) ??
    SNAME_ATTR,  # friendly name
    SUBTYP_ATTR,  # 'ICHLOR' for IntelliChlor, 'ICHEM' for IntelliChem
    SUPER_ATTR,  # (ON/OFF) IntelliChlor: turn on Boost mode (aka Super Chlorinate)
    TIMOUT_ATTR,  # (int) IntelliChlor: in seconds ??
}
CIRCGRP_ATTRIBUTES = {
    ACT_ATTR,
    CIRCUIT_ATTR,
    DLY_ATTR,
    LISTORD_ATTR,
    PARENT_ATTR,
    READY_ATTR,
    STATIC_ATTR,
}

CIRCUIT_ATTRIBUTES = {
    ACT_ATTR,  # to be set for changing USE attribute
    BODY_ATTR,
    "CHILD",
    "COVER",
    "DNTSTP",  # (ON/OFF) "Don't Stop", disable egg timer
    FEATR_ATTR,  # (ON/OFF) Featured
    "FREEZE",  # (ON/OFF) Freeze Protection
    HNAME_ATTR,  # equals to OBJNAM
    "LIMIT",
    LISTORD_ATTR,  # (int) used to order in UI
    "OBJLIST",
    PARENT_ATTR,  # OBJNAM of the parent object
    READY_ATTR,  # (ON/OFF) ??
    SELECT_ATTR,  # ???
    "SET",  # (ON/OFF) for light groups only
    SHOMNU_ATTR,  # (str) permissions
    SNAME_ATTR,  # (str) friendly name
    STATIC_ATTR,  # (ON/OFF) ??
    STATUS_ATTR,  # (ON/OFF) 'ON' if circuit is active
    SUBTYP_ATTR,  # subtype can be '?
    "SWIM",  # (ON/OFF) for light groups only
    "SYNC",  # (ON/OFF) for light groups only
    TIME_ATTR,  # (int) Egg Timer, number of minutes
    "USAGE",
    USE_ATTR,  # for lights with light effects, indicate the 'color'
}

# represents External Equipment like covers
EXTINSTR_ATRIBUTES = {
    BODY_ATTR,  # (objnam) which body it covers
    HNAME_ATTR,  # equals to OBJNAM
    LISTORD_ATTR,  # (int) used to order in UI
    NORMAL_ATTR,  # (ON/OFF) 'ON' for Cover State Normally On
    PARENT_ATTR,  # (objnam)
    READY_ATTR,  # (ON/OFF) ???
    SNAME_ATTR,  # (str) friendly name
    STATIC_ATTR,  # (ON/OFF) 'OFF'
    STATUS_ATTR,  # (ON/OFF) 'ON' if cover enabled
    SUBTYP_ATTR,  # only seen 'COVER'
}

# no idea what this represents
FEATR_ATTRIBUTES = {
    HNAME_ATTR,
    LISTORD_ATTR,
    READY_ATTR,
    SNAME_ATTR,
    SOURCE_ATTR,
    STATIC_ATTR,
}

HEATER_ATTRIBUTES = {
    BODY_ATTR,  # the objnam of the body the pump serves or a list (separated by a space)
    "BOOST",  # (int) ??
    COMUART_ATTR,  # X25 related?
    "COOL",  # (ON/OFF)
    DLY_ATTR,  # (int) ??
    HNAME_ATTR,  # equals to OBJNAM
    HTMODE_ATTR,  # (int) ??
    LISTORD_ATTR,  # (int) used to order in UI
    PARENT_ATTR,  # (objnam) parent (module) for this heater
    READY_ATTR,  # (ON/OFF)
    SHOMNU_ATTR,  # (str) permissions
    SNAME_ATTR,  # (str) friendly name
    "START",  # (int) ??
    STATIC_ATTR,  # (ON/OFF) 'OFF'
    STATUS_ATTR,  # (ON/OFF) only seen 'ON'
    "STOP",  # (int) ??
    SUBTYP_ATTR,  # type of heater 'GENERIC','SOLAR','ULTRA','HEATER'
    TIME_ATTR,  # (int) ??
}

MODULE_ATTRUBUTES = {
    "CIRCUITS",  # [ objects ] the objects that the module controls
    PARENT_ATTR,  # (objnam) the parent (PANEL) of the module
    "PORT",  # (int) no idea
    SNAME_ATTR,  # friendly name
    STATIC_ATTR,  # (ON/OFF) 'ON'
    SUBTYP_ATTR,  # type of the module (like 'I5P' or 'I8PS')
    VER_ATTR,  # (str) the version of the firmware for this module
}

PANEL_ATTRIBUTES = {
    HNAME_ATTR,  # equals to OBJNAM
    LISTORD_ATTR,  # (int) used to order in UI
    "OBJLIST",  # [ (objnam) ] the elements managed by the panel
    "PANID",  # ??? only seen 'SHARE'
    SNAME_ATTR,  # friendly name
    STATIC_ATTR,  # only seen 'ON'
    SUBTYP_ATTR,  # only seen 'OCP'
}

# represent a USER for the system
PERMIT_ATTRIBUTES = {
    ENABLE_ATTR,  # (ON/OFF) ON if user is enabled
    "PASSWRD",  # 4 digit code or ''
    SHOMNU_ATTR,  # privileges associated with this user
    SNAME_ATTR,  # friendly name
    STATIC_ATTR,  # (ON/OFF) only seen ON
    SUBTYP_ATTR,  # ADV for administrator, BASIC for guest
    TIMOUT_ATTR,  # (int) in minutes, timeout for user session
}

# represents a PUMP setting
PMPCIRC_ATTRIBUTES = {
    BODY_ATTR,  # not sure, I've only see '00000'
    CIRCUIT_ATTR,  # (objnam) the circuit this setting is for
    GPM_ATTR,  # (int): the flow setting for the pump if select is GPM
    LISTORD_ATTR,  # (int) used to order in UI
    PARENT_ATTR,  # (objnam) the pump the setting belongs to
    "SPEED",  # (int): the speed setting for the pump if select is RPM
    SELECT_ATTR,  # 'RPM' or 'GPM'
}

# no idea what this object type represents
# only seem to be one instance of it
PRESS_ATTRIBUTES = {
    SHOMNU_ATTR,  # (ON/OFF) ???
    SNAME_ATTR,  # seems equal to objnam
    STATIC_ATTR,  # (ON/OFF) only seen ON
}

# represents a PUMP
PUMP_ATTRIBUTES = {
    BODY_ATTR,  # the objnam of the body the pump serves or a list (separated by a space)
    CIRCUIT_ATTR,  # (int) ??? only seen 1
    COMUART_ATTR,  # X25 related?
    HNAME_ATTR,  # same as objnam
    GPM_ATTR,  # (int) when applicable, real time Gallon Per Minute
    LISTORD_ATTR,  # (int) used to order in UI
    "MAX",  # (int) maximum RPM
    "MAXF",  # (int) maximum GPM (if applicable, 0 otherwise)
    "MIN",  # (int) minimum RPM
    "MINF",  # (int) minimum GPM (if applicable, 0 otherwise)
    "NAME",  # seems to equal OBJNAM
    "OBJLIST",  # ([ objnam] ) a list of PMPCIRC settings
    "PRIMFLO",  # (int) Priming Speed
    "PRIMTIM",  # (int) Priming Time in minutes
    "PRIOR",  # (int) ???
    PWR_ATTR,  # (int) when applicable, real time Power usage in Watts
    RPM_ATTR,  # (int) when applicable, real time Rotation Per Minute
    "SETTMP",  # (int) Step size for RPM
    "SETTMPNC",  # (int) ???
    SNAME_ATTR,  # friendly name
    STATUS_ATTR,  # only seen 10 for on, 4 for off
    SUBTYP_ATTR,  # type of pump: 'SPEED' (variable speed), 'FLOW' (variable flow), 'VSF' (both)
    "SYSTIM",  # (int) ???
}


# represents a mapping between a remote button and a circuit
REMBTN_ATTRIBUTES = {
    CIRCUIT_ATTR,  # (objnam) the circuit triggered by the button
    LISTORD_ATTR,  # (int) which button on the remote (1 to 4)
    PARENT_ATTR,  # (objnam) the remote this button is associated with
    STATIC_ATTR,  # (ON/OFF) not sure, only seen 'ON'
}

# represents a REMOTE
REMOTE_ATTRIBUTES = {
    BODY_ATTR,  # (objnam) the body the remote controls
    COMUART_ATTR,  # X25 address?
    ENABLE_ATTR,  # (ON/OFF) 'ON' if the remote is set to active
    HNAME_ATTR,  # same as objnam
    LISTORD_ATTR,  # number likely used to order things in UI
    SNAME_ATTR,  # friendly name
    STATIC_ATTR,  # (ON/OFF) not sure, only seen 'OFF'
    SUBTYP_ATTR,  # type of the remote, I've only seen IS4
}

# represents a SCHEDULE
SCHED_ATTRIBUTES = {
    ACT_ATTR,  # (ON/OFF) ON is schedule is currently active
    CIRCUIT_ATTR,  # (objnam) the circuit controlled by this schedule
    "DAY",  # the days this schedule run (example: 'MTWRFAU' for every day, 'AU' for weekends)
    "DNTSTP",  # 'ON' or 'OFF" means Don't Stop. Set to ON to never end...
    HEATER_ATTR,  # set to a HEATER objnam is the schedule should trigger heating, '00000' for off, '00001' for Don't Change
    HNAME_ATTR,  # same as objnam
    "HITMP",  # number but not sure
    LISTORD_ATTR,  # number likely used to order things in UI
    LOTMP_ATTR,  # number. when heater is set, that is the desired temperature
    "SINGLE",  # 'ON' if the schedule is not to repeat
    SNAME_ATTR,  # the friendly name of the schedule
    "START",  # start time mode
    # 'ABSTIM' means absolute and 'TIME' will be the startime
    # 'SRIS' means Sunrise, 'SSET' means Sunset
    STATIC_ATTR,  # (ON/OFF) not sure, only seen 'OFF'
    STATUS_ATTR,  # 'ON' if schedule is active, 'OFF' otherwise
    "STOP",  # stop time mode ('ABSTIME','SRIS' or 'SSET')
    TIME_ATTR,  # time the schedule starts in 'HH,MM,SS' format (24h clock)
    TIMOUT_ATTR,  # time the schedule stops in 'HH,MM,SS' format (24h clock)
    VACFLO_ATTR,  # (ON/OFF) 'ON' if schedule only applies to Vacation Mode
}

# represents a SENSOR
SENSE_ATTRIBUTES = {
    "CALIB",  # (int) calibration value
    HNAME_ATTR,  # same as objnam
    LISTORD_ATTR,  # number likely used to order things in UI
    MODE_ATTR,  # I've only seen 'OFF' so far
    "NAME",  # I've only seen '00000'
    PARENT_ATTR,  # the parent's objnam
    "PROBE",  # the uncalibrated reading of the sensor
    SNAME_ATTR,  # friendly name
    SOURCE_ATTR,  # the calibrated reading of the sensor
    STATIC_ATTR,  # (ON/OFF) not sure, only seen 'ON'
    STATUS_ATTR,  # I've only seen 'OK' so far
    SUBTYP_ATTR,  # 'SOLAR','POOL' (for water), 'AIR'
}

# represent the (unique instance of) SYSTEM object
SYSTEM_ATTRIBUTES = [
    ACT_ATTR,  # ON/OFF but not sure what it does
    "ADDRESS",  # Pool Address
    "AVAIL",  # ON/OFF but not sure what it does
    "CITY",  # Pool City
    "COUNTRY",  # Country obviously (example 'United States')
    "EMAIL",  # primary email for the owner
    "EMAIL2",  # secondary email for the owner
    "HEATING",  # ON/OFF: Pump On During Heater Cool-Down Delay
    HNAME_ATTR,  # same as objnam
    "LOCX",  # (float) longitude
    "LOCY",  # (float) latitude
    "MANHT",  # ON/OFF: Manual Heat
    MODE_ATTR,  # unit system, 'METRIC' or 'ENGLISH'
    "NAME",  # name of the owner
    "PASSWRD",  # a 4 digit password or ''
    "PHONE",  # primary phone number for the owner
    "PHONE2",  # secondary phone number for the owner
    PROPNAME_ATTR,  # name of the property
    "SERVICE",  # 'AUTO' for automatic
    SNAME_ATTR,  # a crazy looking string I assume to be unique to this system
    "START",  # almost looks like a date but no idea
    "STATE",  # Pool State
    STATUS_ATTR,  # ON/OFF
    "STOP",  # same value as START
    "TEMPNC",  # ON/OFF
    "TIMZON",  # (int) Time Zone (example '-8' for US Pacific)
    VACFLO_ATTR,  # ON/OFF, vacation mode
    "VACTIM",  # ON/OFF
    "VALVE",  # ON/OFF: Pump Off During Valve Action
    VER_ATTR,  # (str) software version
    "ZIP",  # Pool Zip Code
]

# represents the system CLOCK
# note that there are 2 clocks in the system
# one only contains the SOURCE attribute
# the other everything but SOURCE
SYSTIM_ATTRIBUTES = {
    "CLK24A",  # clock mode, 'AMPM' or 'HR24'
    "DAY",  # in 'MM,DD,YY' format
    "DLSTIM",  # ON/OFF, ON for following DST
    HNAME_ATTR,  # same as objnam
    "LOCX",  # (float) longitude
    "LOCY",  # (float) latitude
    "MIN",  # in 'HH,MM,SS' format (24h clock)
    SNAME_ATTR,  # unused really, likely equals to OBJNAM
    SOURCE_ATTR,  # set to URL if time is from the internet
    STATIC_ATTR,  # (ON/OFF) not sure, only seen 'ON'
    "TIMZON",  # (int) timezone (example '-8' for US Pacific)
    "ZIP",  # ZipCode
}

VALVE_ATTRIBUTES = {
    "ASSIGN",  # 'NONE', 'INTAKE' or 'RETURN'
    CIRCUIT_ATTR,  # I've only seen '00000'
    DLY_ATTR,  # (ON/OFF)
    HNAME_ATTR,  # same as objnam
    PARENT_ATTR,  # (objnam) parent (a module)
    SNAME_ATTR,  # friendly name
    STATIC_ATTR,  # (ON/OFF) I've only seen 'OFF'
    SUBTYP_ATTR,  # I've only seen 'LEGACY'
}

ALL_ATTRIBUTES_BY_TYPE = {
    BODY_TYPE: BODY_ATTRIBUTES,
    CHEM_TYPE: CHEM_ATTRIBUTES,
    CIRCGRP_TYPE: CIRCGRP_ATTRIBUTES,
    CIRCUIT_TYPE: CIRCUIT_ATTRIBUTES,
    "EXTINSTR": EXTINSTR_ATRIBUTES,
    "FEATR": FEATR_ATTRIBUTES,
    HEATER_TYPE: HEATER_ATTRIBUTES,
    "MODULE": MODULE_ATTRUBUTES,
    "PANEL": PANEL_ATTRIBUTES,
    PMPCIRC_TYPE: PMPCIRC_ATTRIBUTES,
    "PRESS": PRESS_ATTRIBUTES,
    PUMP_TYPE: PUMP_ATTRIBUTES,
    REMBTN_TYPE: REMBTN_ATTRIBUTES,
    REMOTE_TYPE: REMOTE_ATTRIBUTES,
    SCHED_TYPE: SCHED_ATTRIBUTES,
    SENSE_TYPE: SENSE_ATTRIBUTES,
    SYSTEM_TYPE: SYSTEM_ATTRIBUTES,
    "SYSTIM": SYSTIM_ATTRIBUTES,
    "VALVE": VALVE_ATTRIBUTES,
}
