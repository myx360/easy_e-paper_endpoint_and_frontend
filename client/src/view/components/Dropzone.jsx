import React, { useCallback } from 'react'
import { makeStyles } from '@material-ui/core/styles';
import { Typography } from '@material-ui/core';
import { grey } from '@material-ui/core/colors';
import { useDropzone } from 'react-dropzone'
import { func } from 'prop-types';

 
const useStyles = makeStyles(theme => ({
  dropzone: {
    border: `dashed 3px ${grey[400]}`,
    borderRadius: 5,
    padding: 5,
  }
}));

const Dropzone = ({ onDropAcceptedCallback }) => {
  const classes = useStyles();
  const onDrop = useCallback((files) => onDropAcceptedCallback(files[0]), [onDropAcceptedCallback])
  const { getRootProps, getInputProps, isDragActive } = useDropzone({onDrop})
 
  return (
    <div className={classes.dropzone} {...getRootProps()}>
      <input {...getInputProps()} />
      {
        isDragActive ?
          <Typography variant="body1">Drop the files here ...</Typography> :
          <Typography variant="body1">Drag 'n' drop your image here, or click to open file-browser</Typography>
      }
    </div>
  )
}

Dropzone.propTypes = {
  onDropAcceptedCallback: func.isRequired
};

export default Dropzone;