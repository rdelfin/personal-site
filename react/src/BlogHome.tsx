/**
 * @format
 */

import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Divider from "@material-ui/core/Divider";
import Typography from "@material-ui/core/Typography";
import Container from "@material-ui/core/Container";

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

export default function BlogHome() {
  const classes = useStyles();

  return (
    <Container maxWidth="md">
      <Card className={classes.root}>
        <CardHeader title="Blog" />
        <CardContent>
          <List
            component="nav"
            className={classes.root}
            aria-label="mailbox folders"
          >
            <ListItem>
              <Typography gutterBottom variant="h6" component="h4">
                Want to browse by topic?
              </Typography>
            </ListItem>
            <ListItem>
              <Typography variant="body2" color="textSecondary" component="p">
                This listing contains all my blog entries in chronological
                order. If you'd rather read them by topic, click below.
              </Typography>
            </ListItem>
            <Divider />
            <ListItem button>
              <ListItemText primary="Blogs by tags" />
            </ListItem>
          </List>
        </CardContent>
      </Card>
    </Container>
  );
}
