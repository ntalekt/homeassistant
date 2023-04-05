// I Used weather-card-editor.js from Weather Card as template
// https://github.com/bramkragten/weather-card
// 2023-02-25 card editor is likely broken as it doesn't show entities,

const fireEvent = (node, type, detail, options) => {
  options = options || {};
  detail = detail === null || detail === undefined ? {} : detail;
  const event = new Event(type, {
    bubbles: options.bubbles === undefined ? true : options.bubbles,
    cancelable: Boolean(options.cancelable),
    composed: options.composed === undefined ? true : options.composed,
  });
  event.detail = detail;
  node.dispatchEvent(event);
  return event;
};

if (
  !customElements.get("ha-switch") &&
  customElements.get("paper-toggle-button")
) {
  customElements.define("ha-switch", customElements.get("paper-toggle-button"));
}

const LitElement = customElements.get("hui-masonry-view") ? Object.getPrototypeOf(customElements.get("hui-masonry-view")) : Object.getPrototypeOf(customElements.get("hui-view"));
const html = LitElement.prototype.html;
const css = LitElement.prototype.css;

const HELPERS = window.loadCardHelpers();

export class AirVisualCardEditor extends LitElement {
  setConfig(config) {
    this._config = { ...config };
  }

  static get properties() {
    return { hass: {}, _config: {} };
  }

  get _air_pollution_level() {
    return this._config.air_pollution_level || "sensor.u_s_air_pollution_level";
  }

  get _air_quality_index() {
    return this._config.air_quality_index || "sensor.u_s_air_quality_index";
  }

  get _main_pollutant() {
    return this._config.main_pollutant || "sensor.u_s_main_pollutant";
  }

  get _country() {
    return this._config.country || "";
  }

  get _city() {
    return this._config.city || "";
  }

  get _icons() {
    return this._config.icons || "/hacsfiles/air-visual-card";
  }

  get _weather() {
    return this._config.weather || "weather.home";
  }

  get _speed_unit() {
    return this._config.speed_unit || "mp/h";
  }
  get _unit_of_measurement() {
    return this._config.unit_of_measurement || "AQI";
  }
  get _hide_title() {
    return this._config.hide_title !== false;
  }

  get _hide_face() {
    return this._config.hide_face !== true;
  }
  get _hide_weather() {
    return this._config.hide_weather !== false;
  }

  // WHAT DOES THIS DO?
  firstUpdated() {
    HELPERS.then(help => {
      if (help.importMoreInfoControl) {
        help.importMoreInfoControl("fan");
      }
    })
  }
  
  render() {
    if (!this.hass) {
      return html``;
    }

    // WHAT DOES THIS DO?
    const entities = Object.keys(this.hass.states).filter(
      (eid) => eid.substr(0, eid.indexOf(".")) === "sensor"
    );

    return html`
      <div class="card-config">
        <div>
          ${customElements.get("ha-entity-picker")
            ? html`
                <ha-entity-picker
                  label="Air Pollution Level Sensor Entity"
                  .hass="${this.hass}"
                  .value="${this._air_pollution_level}"
                  .configValue=${"air_pollution_level"}
                  domain-filter="sensor"
                  @change="${this._valueChanged}"
                  allow-custom-entity
                ></ha-entity-picker>
              `
            : html``}

                <ha-entity-picker
                  label="Air Quality Index Sensor"
                  .hass="${this.hass}"
                  .value="${this._air_quality_index}"
                  .configValue=${"air_quality_index"}
                  domain-filter="sensor"
                  @change="${this._valueChanged}"
                  allow-custom-entity
                ></ha-entity-picker>

                <ha-entity-picker
                  label="Main Pollutant Sensor"
                  .hass="${this.hass}"
                  .value="${this._main_pollutant}"
                  .configValue=${"main_pollutant"}
                  domain-filter="sensor"
                  @change="${this._valueChanged}"
                  allow-custom-entity
                ></ha-entity-picker>

                <ha-entity-picker
                  label="Weather Entity (Optional)"
                  .hass="${this.hass}"
                  .value="${this._weather}"
                  .configValue=${"weather"}
                  @change="${this._valueChanged}"
                  allow-custom-entity
                ></ha-entity-picker>                

          <paper-input
            label="City Name (Optional)"
            .value="${this._city}"
            .configValue="${"city"}"
            @value-changed="${this._valueChanged}"
          ></paper-input>

          <paper-input
            label="Country Name (Optional)"
            .value="${this._country}"
            .configValue="${"country"}"
            @value-changed="${this._valueChanged}"
          ></paper-input>

          <paper-input
            label="Speed Unit (Optional)"
            .value="${this._speed_unit}"
            .configValue="${"speed_unit"}"
            @value-changed="${this._valueChanged}"
          ></paper-input>

          <paper-input
          label="Unit of Measurement (Optional)"
          .value="${this._unit_of_measurement}"
          .configValue="${"unit_of_measurement"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>

          <paper-input
            label="Icons location (Optional)"
            .value="${this._icons}"
            .configValue="${"icons"}"
            @value-changed="${this._valueChanged}"
          ></paper-input>

          <div class="switches">
            <div class="switch">
              <ha-switch
                .checked=${this._hide_title}
                .configValue="${"hide_title"}"
                @change="${this._valueChanged}"
              ></ha-switch
              ><span>Hide Title</span>
            </div>
            <div class="switch">
            <ha-switch
              .checked=${this._hide_weather}
              .configValue="${"hide_weather"}"
              @change="${this._valueChanged}"
            ></ha-switch
            ><span>Hide Weather</span>
          </div>
            <div class="switch">
              <ha-switch
                .checked=${this._hide_face}
                .configValue="${"hide_face"}"
                @change="${this._valueChanged}"
              ></ha-switch
              ><span>Hide Face</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  _valueChanged(ev) {
    if (!this._config || !this.hass) {
      return;
    }
    const target = ev.target;
    if (this[`_${target.configValue}`] === target.value) {
      return;
    }
    if (target.configValue) {
      if (target.value === "") {
        delete this._config[target.configValue];
      } else {
        this._config = {
          ...this._config,
          [target.configValue]:
            target.checked !== undefined ? target.checked : target.value,
        };
      }
    }
    fireEvent(this, "config-changed", { config: this._config });
  }

  static get styles() {
    return css`
      .switches {
        margin: 8px 0;
        display: flex;
        justify-content: space-between;
      }
      .switch {
        display: flex;
        align-items: center;
        justify-items: center;
      }
      .switches span {
        padding: 0 16px;
      }
    `;
  }
}

customElements.define("air-visual-card-editor", AirVisualCardEditor);
