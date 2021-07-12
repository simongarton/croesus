import { Navbar, Nav, Container } from 'react-bootstrap';

const Navigation = () => {
  return (
    <>
      <Navbar collapseOnSelect fixed="top" expand="sm" className="background">
        <Container>
          <Navbar.Brand>
            <img
              src="/croesus-one.png"
              width="30"
              height="30"
              className="d-inline-block align-top navigation-bar"
              alt="React Bootstrap logo"
            />
            &nbsp;croesus
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav"></Navbar.Toggle>
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav>
              <Nav.Link href="home">Home</Nav.Link>
              <Nav.Link href="all">All</Nav.Link>
              <Nav.Link href="helen">Helen</Nav.Link>
              <Nav.Link href="simon">Simon</Nav.Link>
              <Nav.Link href="trust">Trust</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  );
};

export default Navigation;
