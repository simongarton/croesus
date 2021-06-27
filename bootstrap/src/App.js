import './App.css';
import { Button, Form } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import { Route, Switch } from 'react-router-dom';

import Home from './pages/Home';
import All from './pages/All';
import Helen from './pages/Helen';
import Simon from './pages/Simon';
import Trust from './pages/Trust';

import Navigation from './components/Navigation';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { loggedIn: this.checkForLoggedIn() };
    this.doLogin = this.doLogin.bind(this);
    this.setPassword = this.setPassword.bind(this);
    this.checkForLoggedIn();
  }

  checkForLoggedIn() {
    const loggedIn = window.sessionStorage.getItem('loggedIn');
    if (loggedIn && loggedIn === 'true') {
      return true;
    }
    return false;
  }

  doLogin = (event) => {
    event.preventDefault();
    if (!this.state.password) {
      return;
    }
    const url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/password';
    var t0 = performance.now();
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
          if (result['code'] === 200) {
            window.sessionStorage.setItem('loggedIn', 'true');
          }
          var t1 = performance.now()
          console.log("Call to " + url + " took " + (t1 - t0) + " milliseconds.")
        },
        (error) => {
          window.sessionStorage.removeItem('loggedIn');
          this.setState({
            response: null,
            loggedIn: false,
            error,
          });
        }
      );
  };

  doLogout = (event) => {
    event.preventDefault();
    this.setState({ loggedIn: false });
    window.sessionStorage.removeItem('loggedIn');
  };

  setPassword(e) {
    this.setState({ password: e.target.value });
  }

  loginForm(imageName) {
    const autoCompleteTag = 'password';
    const controlIdTag = 'password';
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
    const loginForm = this.loginForm('croesus.png');
    return <div className="App">{loginForm}</div>;
  }

  mainBody() {
    const logoutForm = this.logoutForm();
    return (
      <>
        <div className="App">
          <Navigation></Navigation>
          <div className="navigationBarSpace">
            <Switch>
              <Route path="/all" component={All} />
              <Route path="/helen" component={Helen} />
              <Route path="/simon" component={Simon} />
              <Route path="/trust" component={Trust} />
              <Route path="/" component={Home} />
            </Switch>
            {logoutForm}
          </div>
        </div>
      </>
    );
  }
}

export default App;
