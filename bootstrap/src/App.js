import './App.css';
import { Button, Container, Row, Col, Card, Form, ButtonGroup } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import TotalValue from './widgets/TotalValue.js';
import TotalValueMobileCard from './widgets/TotalValueMobileCard.js';
import TotalValueLineMobileCard from './widgets/TotalValueLineMobileCard.js';
import GainLossLineMobileCard from './widgets/GainLossLineMobileCard.js';

const DESKTOP = 1;
const MOBILE = 0;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { loggedIn: false, account: 'all' };
    this.doLogin = this.doLogin.bind(this);
    this.setPassword = this.setPassword.bind(this);
    this.accountChange = this.accountChange.bind(this);
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

  mainDetails(index) {
    if (this.mainDetails === DESKTOP) {
      return this.mainDetailsDesktop();
    }
    return this.mainDetailsMobile();
  }

  accountChange(event) {
    console.log(event);
    console.log(event.target.outerText);
    this.setState({ account: event.target.outerText });
  }

  toggleButtonGroup() {
    return (
      <ButtonGroup className="mb-2">
        <Button variant="secondary" onClick={this.accountChange}>
          all
        </Button>
        <Button variant="secondary" onClick={this.accountChange}>
          helen
        </Button>
        <Button variant="secondary" onClick={this.accountChange}>
          simon
        </Button>
        <Button variant="secondary" onClick={this.accountChange}>
          trust
        </Button>
      </ButtonGroup>
    );
  }

  mainDetailsDesktop() {
    return (
      <div className="mt-1">
        {this.toggleButtonGroup()}
        <TotalValue account="all"></TotalValue>
      </div>
    );
  }

  mainDetailsMobile() {
    return (
      <div className="mt-1">
        {this.toggleButtonGroup()}
        <TotalValueMobileCard account={this.state.account}></TotalValueMobileCard>
        <TotalValueLineMobileCard account={this.state.account}></TotalValueLineMobileCard>
        <GainLossLineMobileCard account={this.state.account}></GainLossLineMobileCard>
      </div>
    );
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
        <Button className="mb-2" variant="secondary" onClick={this.doLogin} type="submit">
          Login
        </Button>
      </div>
    );
  }

  logoutForm() {
    return (
      <Form className="mb-1" onSubmit={this.doLogout}>
        <Button variant="secondary" type="submit">
          Logout
        </Button>
      </Form>
    );
  }

  body(index, imageName) {
    var details;
    var loginForm;
    var logoutForm;
    if (this.state.loggedIn) {
      details = this.mainDetails(index);
      loginForm = <div />;
      logoutForm = this.logoutForm(index);
    } else {
      details = <div />;
      loginForm = this.loginForm(index, imageName);
      logoutForm = <div />;
    }
    return (
      <Container>
        <Row>
          <Col>
            {loginForm}
            {details}
            {logoutForm}
          </Col>
        </Row>
      </Container>
    );
  }

  render() {
    return (
      <div className="App vertical-center" key={this.state.account}>
        <div className="hide-on-mobile">{this.body(DESKTOP, 'croesus-large.jpeg')}</div>
        <div className="hide-on-desktop">{this.body(MOBILE, 'croesus.png')}</div>
      </div>
    );
  }
}

export default App;
