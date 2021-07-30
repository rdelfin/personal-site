/**
 * @format
 */

import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import Container from "@material-ui/core/Container";
import Grid from "@material-ui/core/Grid";

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

export default function Home() {
  const classes = useStyles();

  return (
    <Container maxWidth="md">
      <Card className={classes.root}>
        <CardHeader title="Projects" />
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography gutterBottom variant="h4" component="h2">
                Projects
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <Typography variant="body2" color="textSecondary" component="p">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque
                feugiat ante non risus aliquet, non facilisis turpis malesuada.
                Morbi eleifend auctor enim vel vestibulum. Nunc consectetur
                gravida nibh, vitae rhoncus justo. Curabitur egestas finibus
                dapibus. Praesent justo risus, iaculis efficitur bibendum
                laoreet, tristique quis eros. Aliquam in justo venenatis,
                laoreet nibh et, dictum mauris. Etiam fermentum felis id velit
                varius sodales. Suspendisse hendrerit eros eget arcu gravida
                facilisis. Integer sit amet enim erat. Donec id iaculis lorem,
                id dignissim justo. Cras non egestas mauris. Donec condimentum
                suscipit diam, et malesuada nisi lacinia in. Aliquam erat
                volutpat. Donec sagittis laoreet felis, eu eleifend ipsum mollis
                sit amet. Nunc in justo pretium, tincidunt magna vel, maximus
                leo. Vivamus efficitur rhoncus mi id tempor. Vivamus dignissim
                nec elit et sagittis. Proin tristique a libero a luctus. Quisque
                condimentum volutpat tristique. Donec mattis mi et dui euismod
                egestas. In fermentum, nibh non rutrum varius, orci sem
                condimentum arcu, non tempus ipsum ligula a elit. Proin ac justo
                sollicitudin, venenatis nunc id, tempor risus. Pellentesque
                vitae nisl at neque congue placerat quis in velit. Phasellus
                venenatis sodales felis, quis maximus nulla consectetur vitae.
                Nam augue lacus, consequat vitae viverra quis, ornare nec dui.
                Cras eget eleifend nulla, vitae consectetur augue. Praesent
                tristique metus convallis libero dictum pellentesque.
                Suspendisse sit amet sem a neque tristique pellentesque ut vitae
                elit.
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Container>
  );
}
