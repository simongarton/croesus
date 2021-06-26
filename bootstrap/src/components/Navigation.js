import { Navbar, Nav, Container } from 'react-bootstrap';

const Navigation = () => {
  return (
    <>
      <Navbar collapseOnSelect fixed="top" expand="sm" bg="dark" variant="dark">
        <Container>
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
