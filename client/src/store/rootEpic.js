import { default as pictureUploadEpics } from '../data/epics';
import { combineEpics } from 'redux-observable';

const rootEpic = combineEpics(pictureUploadEpics);

export default rootEpic;
