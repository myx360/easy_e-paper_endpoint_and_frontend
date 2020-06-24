import { connect } from 'react-redux';
import Dropzone from '../components/Dropzone';
import actions from '../../data/actions';


const dispatchToProps = (dispatch) => ({
  onDropAcceptedCallback: (file) => dispatch(actions.pictureUploadRequest(file)),
});

export default connect(null, dispatchToProps)(Dropzone);
