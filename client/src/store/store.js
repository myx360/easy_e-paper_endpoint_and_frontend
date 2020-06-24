import { createStore, applyMiddleware } from 'redux';
import rootReducer from './rootReducer';
import rootEpic from './rootEpic';
import { requester } from '../util'
import { createEpicMiddleware } from 'redux-observable';
import { composeWithDevTools } from 'redux-devtools-extension';


const epics = createEpicMiddleware({
  dependencies: requester
});
const middleware = applyMiddleware(epics);

const devToolsOptions = {
  name: 'Epaper Display App',
  shouldCatchErrors: true,
};
const enhancers = composeWithDevTools(devToolsOptions)(middleware);

const store = createStore(rootReducer, enhancers);

epics.run(rootEpic);

export { store };