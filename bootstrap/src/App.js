import './App.css';
import { Button, Container, Form, ButtonGroup } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import { Route, Switch } from 'react-router-dom';

import Home from './pages/Home';
import All from './pages/All';
import Helen from './pages/Helen';
import Simon from './pages/Simon';
import Trust from './pages/Trust';

const DESKTOP = 1;
const MOBILE = 0;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { loggedIn: false, account: 'all' };
    this.doLogin = this.doLogin.bind(this);
    this.setPassword = this.setPassword.bind(this);
  }

  doLogin = (event) => {
    event.preventDefault();
    const url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/password';
    fetch(url, {
      method: 'POST',
      body: '{"password":"' + this.state.password + '"}',
    })
      // res is the CORS response and gives me a 200
      .then((res) => res.json())
      .then(
        // result is the body - and I have no status code !
        (result) => {
          this.setState({
            response: result,
            loggedIn: result['code'] === 200,
          });
        },
        (error) => {
          this.setState({
            response: null,
            loggedIn: false,
            error,
          });
        }
      );
    this.setState({ loggedIn: true });
  };

  doLogout = (event) => {
    event.preventDefault();
    this.setState({ loggedIn: false });
  };

  setPassword(e) {
    this.setState({ password: e.target.value });
  }

  loginForm(index, imageName) {
    const autoCompleteTag = 'password' + index;
    const controlIdTag = 'password' + index;
    return (
      <div>
        <img alt="croesus" src={imageName} className="small-logo" />

        <Form className="mb-1" onSubmit={this.doLogin}>
          <Form.Group controlId={controlIdTag}>
            <Form.Control
              type="password"
              placeholder="Enter password"
              onChange={this.setPassword}
              autoComplete={autoCompleteTag}
            ></Form.Control>
          </Form.Group>
        </Form>
        <Button className="mb-2" variant="primary" onClick={this.doLogin} type="submit">
          Login
        </Button>
      </div>
    );
  }

  logoutForm() {
    return (
      <Form className="mb-1" onSubmit={this.doLogout}>
        <Button variant="primary" type="submit">
          Logout
        </Button>
      </Form>
    );
  }

  render() {
    if (this.state.loggedIn) {
      return this.mainBody();
    }
    const loginForm = this.loginForm(MOBILE, 'croesus.png');
    return <div className="App">{loginForm}</div>;
  }

  mainBody() {
    const logoutForm = this.logoutForm(MOBILE);
    return (
      <>
        <div className="App">
          <Switch>
            <Route path="/all" component={All} />
            <Route path="/helen" component={Helen} />
            <Route path="/simon" component={Simon} />
            <Route path="/trust" component={Trust} />
            <Route path="/" component={Home} />
          </Switch>
          {logoutForm}
        </div>
      </>
    );
  }
}

export default App;
