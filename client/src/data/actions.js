import { createAction } from 'redux-actions';

export const PICTURE_UPLOAD_REQUEST = 'PICTURE_UPLOAD_REQUEST';
export const PICTURE_UPLOAD_SUCCESS = 'PICTURE_UPLOAD_SUCCESS';
export const PICTURE_UPLOAD_FAILURE = 'PICTURE_UPLOAD_FAILURE';
export const PICTURE_UPLOAD_RESET_DATA = 'PICTURE_UPLOAD_RESET_DATA';
export const PICTURE_UPLOAD_RESET_ERROR = 'PICTURE_UPLOAD_RESET_ERROR';

export const pictureUploadRequest = createAction(PICTURE_UPLOAD_REQUEST);
export const pictureUploadSuccess = createAction(
  PICTURE_UPLOAD_SUCCESS,
  (preview) => (preview)
);
export const pictureUploadFailure = createAction(
  PICTURE_UPLOAD_FAILURE,
  (err) => (err)
);
export const pictureUploadResetData = createAction(PICTURE_UPLOAD_RESET_DATA);
export const pictureUploadResetError = createAction(PICTURE_UPLOAD_RESET_ERROR);

export default {
  pictureUploadRequest, pictureUploadSuccess, pictureUploadResetData, pictureUploadResetError
};