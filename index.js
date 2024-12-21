/**
 * @format
 */

import {AppRegistry} from 'react-native';
import App from './App';
import {name as appName} from './app.json';

AppRegistry.registerComponent(appName, () => App);

const Rec = async (data) => {
  console.log('It works!', data);
};

AppRegistry.registerHeadlessTask('Rec', () => Rec);
