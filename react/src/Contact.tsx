/**
 * @format
 */

import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardHeader from "@material-ui/core/CardHeader";
import Container from "@material-ui/core/Container";
import Grid from "@material-ui/core/Grid";
import SendIcon from "@material-ui/icons/Send";
import TextField from "@material-ui/core/TextField";
import Typography from "@material-ui/core/Typography";

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

export default function Contact() {
  const classes = useStyles();

  return (
    <Container maxWidth="md">
      <Card className={classes.root}>
        <CardHeader title="Contact" />
        <CardContent>
          <form className={classes.root} noValidate autoComplete="off">
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary" component="p">
                  Shoot me an email through this form!
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <TextField id="name" label="Your Name" />
              </Grid>
              <Grid item xs={12}>
                <TextField id="email" label="Your email" type="email" />
              </Grid>
              <Grid item xs={12}>
                <TextField id="subject" label="Subject" />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  id="content"
                  label="Content"
                  multiline
                  rows={10}
                  fullWidth
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12}>
                <Button
                  variant="contained"
                  color="primary"
                  endIcon={<SendIcon />}
                >
                  Send
                </Button>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>
    </Container>
  );
}
