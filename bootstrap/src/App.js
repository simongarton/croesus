import './App.css';
import { Button, Container, Row, Col, Card, Form } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import TotalValue from './widgets/TotalValue.js';
import TotalValueMobileCard from './widgets/TotalValueMobileCard.js';

const DESKTOP = 1;
const MOBILE = 0;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { loggedIn: false };
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

  mainDetails(index) {
    if (this.mainDetails === DESKTOP) {
      return this.mainDetailsDesktop();
    }
    return this.mainDetailsMobile();
  }

  mainDetailsDesktop() {
    return (
      <div>
        <TotalValue account="all"></TotalValue>
      </div>
    );
  }

  mainDetailsMobile() {
    return (
      <div>
        <TotalValueMobileCard></TotalValueMobileCard>
      </div>
    );
  }

  loginForm(index) {
    const autoCompleteTag = 'password' + index;
    const controlIdTag = 'password' + index;
    return (
      <Form className="mb-3" onSubmit={this.doLogin}>
        <Form.Group controlId={controlIdTag}>
          <Form.Control
            type="password"
            placeholder="Enter password"
            onChange={this.setPassword}
            autoComplete={autoCompleteTag}
          ></Form.Control>
        </Form.Group>
        <Button type="submit">Login</Button>
      </Form>
    );
  }

  logoutForm() {
    return (
      <Form className="mb-3" onSubmit={this.doLogout}>
        <Button type="submit">Logout</Button>
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
      loginForm = this.loginForm(index);
      logoutForm = <div />;
    }
    return (
      <Container>
        <Row>
          <Col>
            <Card className="mb-3">
              <Card.Img src={imageName} />
              <Card.Title>croesus</Card.Title>
            </Card>
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
      <div className="App">
        <div className="hide-on-mobile">{this.body(DESKTOP, 'croesus-large.jpeg')}</div>
        <div className="hide-on-desktop">{this.body(MOBILE, 'croesus.jpeg')}</div>
      </div>
    );
  }
}

export default App;
