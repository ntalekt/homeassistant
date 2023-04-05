// To study:
// Plant Picture Card: https://github.com/badguy99/PlantPictureCard/blob/master/dist/PlantPictureCard.js
// UPDATE FOR EACH RELEASE!!! From aftership-card. Version # is hard-coded for now.
console.info(
  `%c  AIR-VISUAL-CARD  \n%c  Version 2.0.2   `,
  'color: orange; font-weight: bold; background: black',
  'color: white; font-weight: bold; background: dimgray',
);

// From weather-card
const fireEvent = (node, type, detail, options) => {
  options = options || {};
  detail = detail === null || detail === undefined ? {} : detail;
  const event = new Event(type, {
    bubbles: options.bubbles === undefined ? true : options.bubbles,
    cancelable: Boolean(options.cancelable),
    composed: options.composed === undefined ? true : options.composed
  });
  event.detail = detail;
  node.dispatchEvent(event);
  return event;
};

let oldStates = {}

class AirVisualCard extends HTMLElement {
//  Placeholder for lovelace card editor
//  static getConfigElement() {
//    return document.createElement("air-visual-card-editor");
//  }

  static async getConfigElement() {
    await import("./air-visual-card-editor.js");
    return document.createElement("air-visual-card-editor");
  }

  static getStubConfig() {
    return { air_pollution_level: "sensor.u_s_air_pollution_level",
             air_quality_index: "sensor.u_s_air_quality_index",
             main_pollutant: "sensor.u_s_main_pollutant",
             weather: "weather.home",
             hide_weather: 1,
             hide_title: 1,
             unit_of_measurement: "AQI",
             hide_face: 0              
    }
  }

    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
    }

    setConfig(config) {
      const root = this.shadowRoot;
      if (root.lastChild) root.removeChild(root.lastChild);

      const re = new RegExp("(sensor)");
      if (!re.test(config.air_quality_index.split('.')[0])) throw new Error('Please define a sensor entity.');


      const cardConfig = Object.assign({}, config);
      const card = document.createElement('ha-card');
      const content = document.createElement('div');
      const style = document.createElement('style');

      style.textContent = `
        ha-card {
          /* sample css */
          background-color: rgba(0,0,0,0);
          box-shadow: none;
        }

        body {
          margin: 0;
          font-family: Arial, Helvetica, sans-serif;
        }

        .grid-container {          
          display: grid;
          grid-template-areas: "city city city" "face aqiSensor aplSensor" "face country mainPollutantSensor" "temp humidity wind";
          grid-template-columns: 85px 30% auto;
          grid-template-rows: auto auto auto auto;
          grid-gap: 0;
          text-align: center;  
        }

        .city {
          grid-area: city;
          font-size: 1.6em;     
          font-weight: bold;   
          color: var(--primary-text-color);
          filter: opacity(80%);
          padding-bottom: 5px;      
        }

        .face {
          border-radius: var(--ha-card-border-radius) 0px 0px ${cardConfig.hide_weather ? 'var(--ha-card-border-radius)' : '0px'};
          grid-area: face;
          justify-items: center;
          align-items: center;
          display: grid;
        }

        .face img {
          display: block;
          height: 60px;         
        }

        .aqiSensor {
          grid-area: aqiSensor;        
          font-size: 3em; 
          height: 60px;
          padding-top: 4px;
          display: flex;
          align-items: center;
          justify-content: center;    
          border-radius: ${cardConfig.hide_face ? 'var(--ha-card-border-radius)' : '0px'} 0px 0px 0px;
        }

        .aplSensor {
          grid-area: aplSensor;
          font-size: 1.4em;         
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 0px var(--ha-card-border-radius) 0px 0px;
        }

        .mainPollutantSensor {
          grid-area: mainPollutantSensor;
          border-radius: 0px 0px ${cardConfig.hide_weather ? 'var(--ha-card-border-radius)' : '0px'} 0px ;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 0px 0px 5px 0px;
        }

        .mainPollutantSensorText {
          background-color: white;
          border-radius: 4px;
          font-size: 0.9em;
          font-weight: bold;
          width: 70%;
        
        }

        .country {
          grid-area: country; 
          border-radius: 0px 0px 0px ${cardConfig.hide_face ? 'var(--ha-card-border-radius)' : '0px'};    
        }

        .temp {
          grid-area: temp;
          text-align: left;
          font-size: 1.2em;     
          background-color: rgba(255,255,255,0.2); 
          color: var(--text-color);
          border-radius: 0px 0px 0px var(--ha-card-border-radius);
          border-bottom: 1px solid rgba(230, 230, 230, 1);
          border-left: 1px solid rgba(230, 230, 230, 1);
          border-right: 1px solid rgba(230, 230, 230, 1);
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .temp img {
          width: 34px;
          padding-right: 2px;
          
        }

        .humidity {
          grid-area: humidity;
          color: var(--text-color);
          border-bottom: 1px solid rgba(230, 230, 230, 1);
          background-color: rgba(255,255,255,0.2); 
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 5px 0px 5px 0px;
        }
        .humidity img {
          height: 25px;     
          padding-right: 2px;           
        }

        .wind {
          grid-area: wind;
          background-color: rgba(255,255,255,0.2); 
          color: var(--text-color);
          border-radius: 0px 0px var(--ha-card-border-radius) 0px;
          border-bottom: 1px solid rgba(230, 230, 230, 1);
          border-right: 1px solid rgba(230, 230, 230, 1);
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .wind img {
          height: 14px;   
          padding-right: 2px;             
        }
      `
      content.innerHTML = `
      <div id='content'>
      </div>
      `;

      card.appendChild(content);
      card.appendChild(style);
      root.appendChild(card);
      oldStates = {}
      this._config = cardConfig;
    }

    shouldNotUpdate(config, hass) {
      let clone = JSON.parse(JSON.stringify(config))
      delete clone["city"]
      delete clone["type"]
      delete clone["icons"]
      delete clone["hide_title"]
      delete clone["hide_face"]
      delete clone["hide_weather"]
      delete clone["weather"]
      delete clone["speed_unit"]
      let states = {}
      for (let entity of Object.values(clone)) {
        states[entity] = hass.states[entity]
      }
      if (JSON.stringify(oldStates) === JSON.stringify(states)) {
        return true
      }
      oldStates = states
      return false
    }

    set hass(hass) {
      const config = this._config;
      const root = this.shadowRoot;
      const card = root.lastChild;
      if (this.shouldNotUpdate(config, hass)) {
        return 
      }

      const hideTitle = config.hide_title ? 1 : 0;
      const hideFace = config.hide_face ? 1 : 0;
      const hideAQI = config.hide_aqi ? 1 : 0;
      const hideAPL = config.hide_apl ? 1 : 0;
      const hideWeather = config.hide_weather || !config.weather ? 1 : 0;
      const speedUnit = config.speed_unit || 'mp/h';
      // points to local directory created by HACS installation
      const iconDirectory = config.icons || "/hacsfiles/air-visual-card";
      const country = config.country || 'US';
      const city = config.city || '';
      const weatherEntity = config.weather || '';
      // value is used as a string instead of integer in order for 
      const aqiSensor = { name: 'aqiSensor', config: config.air_quality_index || null, value: 0 };
      const aplSensor = { name: 'aplSensor', config: config.air_pollution_level || null, value: 0 };
      const mainPollutantSensor = { name: 'mainPollutantSensor', config: config.main_pollutant || null, value: 0 };
      const sensorList = [aqiSensor, aplSensor, mainPollutantSensor];
      
      const unitOfMeasurement = config.unit_of_measurement || 'AQI';

      const AQIbgColor = {

        '1': `#B0E867`,
        '2': '#E3C143',
        '3': '#E48B4E',
        '4': '#E45F5E',
        '5': '#986EA9',
        '6': '#A5516B',
      };
      const AQIfaceColor = {
        '1': `#A8E05F`,
        '2': '#FDD64B',
        '3': '#FF9B57',
        '4': '#FE6A69',
        '5': '#A97ABC',
        '6': '#A87383',
      };
      const AQIfontColor = {
        '1': `#718B3A`,
        '2': '#A57F23',
        '3': '#B25826',
        '4': '#AF2C3B',
        '5': '#634675',
        '6': '#683E51',
      };

      const weatherIcons = {
        'clear-night': 'mdi:weather-night',
        'cloudy': 'mdi:weather-cloudy',
        'fog': 'mdi:weather-fog',
        'hail': 'mdi:weather-hail',
        'lightning': 'mdi:weather-lightning',
        'lightning-rainy': 'mdi:weather-lightning-rainy',
        'partlycloudy': 'mdi:weather-partly-cloudy',
        'pouring': 'mdi:weather-pouring',
        'rainy': 'mdi:weather-rainy',
        'snowy': 'mdi:weather-snowy',
        'snowy-rainy': 'mdi:weather-snowy-rainy',
        'sunny': 'mdi:weather-sunny',
        'windy': 'mdi:weather-windy',
        'windy-variant': `mdi:weather-windy-variant`,
        'exceptional': '!!',
      }
      const weatherSVG = {
        'clear-night': 'night-clear-sky',
        'cloudy': 'scattered-clouds',
        'fog': 'scattered-clouds',
        'hail': 'rain',
        'lightning': 'rain',
        'lightning-rainy': 'rain',
        'partlycloudy': 'new-clouds',
        'pouring': 'rain',
        'rainy': 'rain',
        'snowy': 'snow',
        'snowy-rainy': 'snow',
        'sunny': 'clear-sky',
        'windy': 'scattered-clouds',
        'windy-variant': `scattered-clouds`,
        'exceptional': 'snow',
      }

      // WAQI sensor-specific stuff
      // AirVisual sensors have the APL description as part of the sensor state, but WAQI doesn't. These APL states will be used as backup if AirVisual sensors is not used.
      const APLdescription = {
        '1': 'Good',
        '2': 'Moderate',
        '3': 'Unhealthy for Sensitive Groups',
        '4': 'Unhealthy',
        '5': 'Very Unhealthy',
        '6': 'Hazardous',
      }
      const pollutantUnitValue = {
        'pm25': 'µg/m³',
        'pm10': 'µg/m³',
        'o3': 'ppb',
        'no2': 'ppb',
        'so2': 'ppb',
      }
      const mainPollutantValue = {
        'p2': 'PM2.5',
        'pm25': 'PM2.5',
        'pm10': 'PM10',
        'o3': 'Ozone',
        'no2': 'Nitrogen Dioxide',
        'so2': 'Sulfur Dioxide',
      }

      let currentCondition = '';
      let humidity = '';
      let windSpeed = '';
      let tempValue = '';
      let pollutantUnit = '';
      let apl = '';
      let mainPollutant = '';

      let getAQI = function () {
        switch (true) {
          case (aqiSensor.value <= 50):
            return '1'; // return string '1' to pull appropriate AQI icon filename ('ic-face-1.svg') in HTML
          case (aqiSensor.value <= 100):
            return '2';
          case (aqiSensor.value <= 150):
            return '3';
          case (aqiSensor.value <= 200):
            return '4';
          case (aqiSensor.value <= 300):
            return '5';
          case (aqiSensor.value <= 9999):
            return '6';
          default:
            return '1';
        }
      };

      var i;
      // Use this section to assign values (real or placeholder), after doing validation check
      for (i = 0; i < sensorList.length; i++) {
        if (typeof hass.states[sensorList[i].config] == "undefined") { continue; }            
        // if Main Pollutant is an Airvisual sensor, else if if it is an WAQI sensor
        if (typeof hass.states[mainPollutantSensor.config] != "undefined") {
          if (typeof hass.states[mainPollutantSensor.config].attributes['pollutant_unit'] != "undefined") {
            pollutantUnit = hass.states[mainPollutantSensor.config].attributes['pollutant_unit'];
            let mainPollutantState = hass.states[mainPollutantSensor.config].state;
            mainPollutant = hass.localize("component.sensor.state.airvisual__pollutant_label." + mainPollutantState);
          } else if (typeof hass.states[mainPollutantSensor.config].attributes['dominentpol'] != "undefined") {
            pollutantUnit = pollutantUnitValue[hass.states[mainPollutantSensor.config].attributes['dominentpol']];
            mainPollutant = mainPollutantValue[hass.states[mainPollutantSensor.config].attributes['dominentpol']];
          } else {
            pollutantUnit = 'pollutant unit';
            mainPollutant = 'main pollutant';
          }         
        }
        if (typeof hass.states[aqiSensor.config] != "undefined") {
          aqiSensor.value = hass.states[aqiSensor.config].state;
        }
        // Check if APL is an WAQI sensor (because the state is an integer). Returns 'NaN' if it is not a number
        if (typeof hass.states[aplSensor.config] != "undefined") {
          let aplParse = parseInt(hass.states[aplSensor.config].state)
          if (!isNaN(aplParse)) {
            apl = APLdescription[getAQI()];      
          } else {
            let aplState = hass.states[aplSensor.config].state;
            apl = hass.localize("component.sensor.state.airvisual__pollutant_level." + aplState)
          }
        }
      };


  




      let faceHTML = ``;

      let card_content = `<div class="grid-container">`;
      if (!hideTitle) {
        card_content += `<div class="city">${city} Air Quality Index</div>`;
      }

      if (weatherEntity.split('.')[0] == 'weather' && hass.states[weatherEntity]) {
        tempValue = hass.states[weatherEntity].attributes['temperature'] + 'º';
        currentCondition = hass.states[weatherEntity].state;
        humidity = hass.states[weatherEntity].attributes['humidity'] + '%';
        windSpeed = hass.states[weatherEntity].attributes['wind_speed'] + ' ' + speedUnit;
      }
      if (!hideWeather) {
        card_content += `
        <div class="temp" id="temp"><img src="${iconDirectory}/ic-w-${weatherSVG[currentCondition]}.svg"></img>${tempValue}</div>
        <div class="humidity" id="humidity"><img src="${iconDirectory}/ic-humidity.svg"></img>${humidity}</div>
        <div class="wind" id="wind"><img src="${iconDirectory}/ic-wind.svg"></img> ${windSpeed}</div>
        `;
      }
      
  
      if (!hideFace){
        card_content += `
          <div class="face" id="face" style="background-color: ${AQIfaceColor[getAQI()]};">
            <img src="${iconDirectory}/ic-face-${getAQI()}.svg"></img>
          </div>
          `;
      }

      if (!hideAQI){
        card_content += `
          <div class="aqiSensor" id="aqiSensor" style="background-color: ${AQIbgColor[getAQI()]}; color: ${AQIfontColor[getAQI()]}">
            ${aqiSensor.value}</div>
          <div class="country" style="background-color: ${AQIbgColor[getAQI()]}; color: ${AQIfontColor[getAQI()]}">${country} ${unitOfMeasurement}</div>
        `;
      }
      if (!hideAPL){        
        card_content += `
          <div class="aplSensor" id="aplSensor" style="background-color: ${AQIbgColor[getAQI()]}; color: ${AQIfontColor[getAQI()]}">
            ${apl}
          </div>
          <div class="mainPollutantSensor" id="mainPollutantSensor" style="background-color: ${AQIbgColor[getAQI()]}; color: ${AQIfontColor[getAQI()]}">
                <div class="mainPollutantSensorText">${mainPollutant} | ${pollutantUnit}</div>    
          </div>     
        `;
      }
      card_content += `
      </div> 
      `;


      root.lastChild.hass = hass;
      root.getElementById('content').innerHTML = card_content;

      // hard-coded version of click event
      if (!hideFace){
	      card.querySelector('#face').addEventListener('click', event => {   // when selecting HTML id, do not use dash '-'
        fireEvent(this, "hass-more-info", { entityId: aqiSensor.config });
        });
      }
      if (!hideAQI){
        card.querySelector('#aqiSensor').addEventListener('click', event => {   // when selecting HTML id, do not use dash '-'
        fireEvent(this, "hass-more-info", { entityId: aqiSensor.config });
        });
      }
      if (!hideAPL){
        card.querySelector('#aplSensor').addEventListener('click', event => {   // when selecting HTML id, do not use dash '-'
          fireEvent(this, "hass-more-info", { entityId: aplSensor.config });
        });
        card.querySelector('#mainPollutantSensor').addEventListener('click', event => {   // when selecting HTML id, do not use dash '-'  
          fireEvent(this, "hass-more-info", { entityId: mainPollutantSensor.config });
        });
      }
    }

    // The height of your card. Home Assistant uses this to automatically
    // distribute all cards over the available columns.
    getCardSize() {
      return 1;
    }
}

customElements.define('air-visual-card', AirVisualCard);

// Configure the preview in the Lovelace card picker
// https://developers.home-assistant.io/docs/frontend/custom-ui/lovelace-custom-card/
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'air-visual-card',
  name: 'Air Visual Card',
  preview: false,
  description: 'This is a Home Assistant Lovelace card that uses the AirVisual Sensor to provide air quality index (AQI) data and creates a card like the ones found on AirVisual website. Requires the AirVisual Sensor to be setup. Tested with Yahoo and Darksky Weather component.'
});
