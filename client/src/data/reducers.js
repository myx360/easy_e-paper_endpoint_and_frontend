import {
 PICTURE_UPLOAD_REQUEST, PICTURE_UPLOAD_SUCCESS, PICTURE_UPLOAD_FAILURE, PICTURE_UPLOAD_RESET_DATA, PICTURE_UPLOAD_RESET_ERROR
} from './actions';

export const initial_state = {
  status: 'idle',
  data: {},
  error: {},
};

const upload = (state = initial_state, action) => {
  switch (action.type) {
    case PICTURE_UPLOAD_REQUEST:
      return { ...state, status: 'running' };
    case PICTURE_UPLOAD_SUCCESS: {
      const data = action.payload;
      return { ...state, status: 'idle', data };
    }
    case PICTURE_UPLOAD_FAILURE: {
      const error = action.payload;
      return { ...state, status: 'idle', error };
    }
    case PICTURE_UPLOAD_RESET_DATA: {
      return { ...state, data: {} };
    }
    case PICTURE_UPLOAD_RESET_ERROR: {
      return { ...state, error: {} };
    }
    default:
      return state;
  }
};

export default upload;