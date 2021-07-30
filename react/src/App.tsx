/**
 * @format
 */

import React from "react";
import { Switch, Route } from "react-router-dom";

import Header from "./Header";
import Home from "./Home";
import Projects from "./Projects";
import Resume from "./Resume";

export default function App() {
  return (
    <Header>
      <Switch>
        <Route path="/projects">
          <Projects />
        </Route>
        <Route path="/resume">
          <Resume />
        </Route>
        <Route path="/">
          <Home />
        </Route>
      </Switch>
    </Header>
  );
}
