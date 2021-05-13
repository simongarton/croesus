import './App.css';
import { Button, Container, Row, Col, Card, Form, ButtonGroup } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import TotalValue from './widgets/TotalValue.js';
import TotalValueMobileCard from './widgets/TotalValueMobileCard.js';

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
      <ButtonGroup className="mb-3">
        <Button onClick={this.accountChange}>all</Button>
        <Button onClick={this.accountChange}>helen</Button>
        <Button onClick={this.accountChange}>simon</Button>
        <Button onClick={this.accountChange}>trust</Button>
      </ButtonGroup>
    );
  }

  mainDetailsDesktop() {
    return (
      <div>
        {this.toggleButtonGroup()}
        <TotalValue account="all"></TotalValue>
      </div>
    );
  }

  mainDetailsMobile() {
    return (
      <div>
        {this.toggleButtonGroup()}
        <TotalValueMobileCard account={this.state.account}></TotalValueMobileCard>
      </div>
    );
  }

  loginForm(index) {
    const autoCompleteTag = 'password' + index;
    const controlIdTag = 'password' + index;
    return (
      <div>
        <Form className="mb-3" onSubmit={this.doLogin}>
          <Form.Group controlId={controlIdTag}>
            <Form.Control
              type="password"
              placeholder="Enter password"
              onChange={this.setPassword}
              autoComplete={autoCompleteTag}
            ></Form.Control>
          </Form.Group>
        </Form>
        <Button onClick={this.doLogin} type="submit">
          Login
        </Button>
      </div>
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
      <div className="App" key={this.state.account}>
        <div className="hide-on-mobile">{this.body(DESKTOP, 'croesus-large.jpeg')}</div>
        <div className="hide-on-desktop">{this.body(MOBILE, 'croesus.jpeg')}</div>
      </div>
    );
  }
}

export default App;
