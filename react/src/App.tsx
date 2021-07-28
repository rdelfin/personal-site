/**
 * @format
 */

import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import Container from "@material-ui/core/Container";
import Grid from "@material-ui/core/Grid";

import Header from "./Header";

const useStyles = makeStyles({
  root: {
    maxWidth: "md",
  },
  media: {
    height: 0,
    paddingTop: "56.25%", // 16:9
  },
  halfImage: {
    maxWidth: "90%",
  },
});

export default function App() {
  const classes = useStyles();

  return (
    <Header>
      <Container maxWidth="md">
        <Card className={classes.root}>
          <CardHeader title="Welcome" />
          <CardMedia
            className={classes.media}
            image="/field.jpg"
            title="The field"
          />
          <CardContent>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography gutterBottom variant="h4" component="h2">
                  Introduction
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="textSecondary" component="p">
                  My name is Ricardo Delfin. I am a Robotics Reliability
                  Engineer at Wayve Technologies Ltd, a startup working to build
                  a scalable self-driving solution using end-to-end machine
                  learning. I am also a Computer Science graduate from the
                  University of Texas at Austin. I am also a Raspberry Pi,
                  robotics, and astronomy enthusiast.
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <img src="/home01.jpg" className={classes.halfImage} />
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Container>
    </Header>
  );
}
