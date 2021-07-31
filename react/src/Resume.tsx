/**
 * @format
 */

import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import Container from "@material-ui/core/Container";
import Grid from "@material-ui/core/Grid";
import { Document, Page } from "react-pdf";

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

export default function Resume() {
  const classes = useStyles();

  return (
    <Container maxWidth="md">
      <Card className={classes.root}>
        <CardHeader title="Resume" />
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Button
                variant="contained"
                color="primary"
                href="/documents/resume.pdf"
              >
                Download
              </Button>
            </Grid>
            <Grid item xs={12}>
              <Document file="/documents/resume.pdf">
                <Page pageNumber={1} scale={1.3} />
              </Document>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Container>
  );
}
