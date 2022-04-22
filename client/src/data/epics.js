import { of } from 'rxjs';
import { mergeMap, catchError } from 'rxjs/operators';
import { ofType, combineEpics } from 'redux-observable';

import {
  PICTURE_UPLOAD_REQUEST, pictureUploadSuccess, pictureUploadResetError, pictureUploadFailure, pictureUploadResetData
} from './actions';

export const pictureUpload = (action$, state$, requester ) => action$.pipe(
  ofType(PICTURE_UPLOAD_REQUEST),
  mergeMap((action) => requester.postImage('picture/display_image', action.payload).pipe(
    mergeMap((result) => of(
      pictureUploadSuccess({ result: result.body, image_black: action.payload }),
      pictureUploadResetError(),
    )),
    catchError((error) => of(
      pictureUploadFailure(error),
      pictureUploadResetData(),
    )),
  )),
);

export default combineEpics(pictureUpload);