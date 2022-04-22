import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Card, CardHeader, CardContent, Grid } from '@material-ui/core';
import Dropzone from './view/containers/Dropzone';
import './App.css';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  title: {
    flexGrow: 1,
  },
}));

function App() {
  const classes = useStyles();

  return (
    <Grid
        container
        spacing={1}
        direction="column"
        alignItems="center"
        justify="center"
        style={{ minHeight: '100vh' }}>

      <Grid item xs={8}>
        <Card variant='outlined' className={classes.root}>
          <CardHeader
              className={classes.title}
              title='E-paper Display'
              titleTypographyProps={{variant: 'h3'}}
              subheader='Picture Upload'
              subheaderTypographyProps={{
                    variant: 'subtitle1',
                    color: 'textSecondary'
                  }}
          />
          <CardContent>
            <Dropzone />
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}

export default App;
