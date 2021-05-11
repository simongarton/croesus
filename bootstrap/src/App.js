import './App.css';
import { Button, Container, Row, Card, Form, Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import TotalValue from './widgets/TotalValue.js';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { loggedIn: false };
  }

  doLogin = (event) => {
    event.preventDefault();
    this.setState({ loggedIn: true });
  };

  doLogout = (event) => {
    event.preventDefault();
    this.setState({ loggedIn: false });
  };

  mainDetails() {
    return (
      <div>
        <TotalValue account="all"></TotalValue>
      </div>
    );
  }

  loginForm() {
    return (
      <Form className="mb-3" onSubmit={this.doLogin}>
        <Form.Group controlId="password">
          <Form.Control type="password" placeholder="Enter password"></Form.Control>
          <Form.Text className="text-muted">secret password to mystical learnings </Form.Text>
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

  render() {
    var details;
    var loginForm;
    var logoutForm;
    if (this.state.loggedIn) {
      details = this.mainDetails();
      loginForm = <div />;
      logoutForm = this.logoutForm();
    } else {
      details = <div />;
      loginForm = this.loginForm();
      logoutForm = <div />;
    }
    return (
      <div className="App">
        <Card className="mb-3">
          <Card.Img src="croesus.jpeg" />
          <Card.Title>croesus</Card.Title>
        </Card>
        {loginForm}
        {details}
        {logoutForm}
      </div>
    );
  }
}

export default App;
