import {
  TabPane,
  Navbar,
  Button,
  Form,
  Nav,
  Spinner,
  FormControl,
  Pagination,
  Collapse,
  OverlayTrigger,
  Popover,
} from "react-bootstrap";
import {
  run_task,
  SearchResults,
  ExportButton,
  AdvancedSearch,
} from "components";
import { useState } from "react";
import { ReactComponent as NestedIcon } from "icons/nested.svg";
import { ReactComponent as InfoIcon } from "icons/info.svg";

export const parseVersioning = (elem) => {
  let longest_property = "captcha";
  let max_versions = 0;
  for (const [key, value] of Object.entries(elem)) {
    if (
      Array.isArray(value) &&
      value.length > max_versions &&
      key !== "mirrors" &&
      key !== "online"
    ) {
      max_versions = value.length;
      longest_property = key;
    }
  }
  const versioned_array = elem[longest_property].map((e, idx) => {
    const captcha = elem.captcha[idx]
      ? elem.captcha[idx]
      : elem.captcha[elem.captcha.length - 1];
    const login = elem.login[idx]
      ? elem.login[idx]
      : elem.login[elem.login.length - 1];
    const crypto = elem.crypto[idx]
      ? elem.crypto[idx]
      : elem.crypto[elem.crypto.length - 1];
    const products = elem.products[idx]
      ? elem.products[idx]
      : elem.products[elem.products.length - 1];
    return {
      date: new Date(e.date),
      title: elem.title,
      captcha: captcha.captcha,
      login: login.login,
      crypto: crypto.crypto,
      products: products.products,
      mirrors: elem.mirrors,
    };
  });
  return versioned_array;
};

const DatabaseTab = (props) => {
  const [searchOutput, setSearchOutput] = useState([]);
  const [activePage, setActivePage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [downloadMode, setDownloadMode] = useState("CSV");
  const [isOpen, setIsOpen] = useState(false);
  const [expressionMode, setExpressionMode] = useState(false);
  const maxPage = Math.ceil(searchOutput.length / 10);

  const handleTask = async (query) => {
    const response = await run_task({
      command: "search",
      query: query,
    }).catch(() => {
      props.toaster(
        "Error",
        "An error occured when trying to launch a search."
      );
    });
    if (response && !(response instanceof Error)) {
      setSearchOutput(response);
      setActivePage(1);
      setLoading(false);
    } else if (response === undefined || response instanceof Error) {
      props.toaster(
        "Error",
        "An error occured when trying to search for " + query
      );
    }
  };

  const handleSubmit = (event) => {
    setLoading(true);
    // Handle onSubmit
    if (event.target.length > 0) {
      event.preventDefault();
      let query = event.target[0].value;
      handleTask(query);
      // Handle onChange
    } else {
      event.preventDefault();
      handleTask(event.target.value);
    }
  };

  const currentPageOutput = () => {
    const currentIndex = activePage - 1;
    return searchOutput.slice(currentIndex * 10, currentIndex * 10 + 10);
  };

  const handlePages = () => {
    let items = [];
    let offset = 0;

    if (maxPage < 4) {
      if (maxPage === 1) return items;
      for (let number = 1; number <= maxPage; number++) {
        items.push(
          <Pagination.Item
            key={number}
            active={number === activePage}
            onClick={() => setActivePage(number)}
          >
            {number}
          </Pagination.Item>
        );
      }
      return items;
    }

    if (activePage - 1 > 1) {
      items.push(
        <Pagination.Prev
          key={"prev"}
          onClick={() => {
            if (activePage > 1) setActivePage(activePage - 1);
          }}
        />
      );
      items.push(
        <Pagination.Ellipsis
          key={"elipsis_p"}
          onClick={() => {
            setActivePage(1);
          }}
        />
      );
    }
    if (activePage - 1 === 0) {
      offset++;
    }
    if (activePage + 1 > maxPage) {
      offset--;
    }
    for (
      let number = activePage - 1 + offset;
      number <= activePage + 1 + offset;
      number++
    ) {
      items.push(
        <Pagination.Item
          key={number}
          active={number === activePage}
          onClick={() => setActivePage(number)}
        >
          {number}
        </Pagination.Item>
      );
    }
    if (activePage + 1 < maxPage) {
      items.push(
        <Pagination.Ellipsis
          key={"elipsis_n"}
          onClick={() => {
            setActivePage(maxPage);
          }}
        />
      );
      items.push(
        <Pagination.Next
          key={"next"}
          onClick={() => {
            if (activePage < maxPage) setActivePage(activePage + 1);
          }}
        />
      );
    }

    return items;
  };

  const helpExpressionMode = (
    <Popover id="helpExpression" style={{ maxWidth: 600 }}>
      <Popover.Title as="h3">Expression Mode</Popover.Title>
      <Popover.Content>
        You can query the database using <strong>expressions</strong> but there
        are a number of rules to follow.
        <br /> The different fields to search are:{" "}
        <strong>
          <code>
            TITLE, LOGIN, CAPTCHA, CRYPTO, PRODUCTS, HTML, ADDRESSES, INDEXERS,
            ONLINE
          </code>
        </strong>
        <br />
        Each field can only by used once.
        <br />
        Use{" "}
        <strong>
          <code>ALL</code>
        </strong>{" "}
        to retrieve the whole database.
        <br />
        Use{" "}
        <strong>
          <code>( )</code>
        </strong>{" "}
        for any operation between <strong>two</strong> logical operators like{" "}
        <strong>
          <code>&&</code>
        </strong>{" "}
        or{" "}
        <strong>
          <code>||</code>
        </strong>
        <br /> Use{" "}
        <strong>
          <code>{"{ }"}</code>
        </strong>{" "}
        for any operation between fields.
        <br />
        Examples: <br />
        <strong>
          <code>{"{ TITLE DEF CON || PRODUCTS Cannabis }"}</code>
        </strong>
        <br />
        <strong>
          <code>
            {
              "{ { TITLE ( Dark || Hack ) && HTML ( Cocaine || Hack ) } && CAPTCHA false }"
            }
          </code>
        </strong>
      </Popover.Content>
    </Popover>
  );

  return (
    <TabPane
      eventKey="#browser"
      onEntered={() => {
        setLoading(true);
        handleTask("");
      }}
    >
      <Navbar bg="light" expand="lg" className="align-items-center">
        <Navbar.Brand href="#home">Database Browser</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link
              onClick={() => {
                window.open("http://root:CZ7DWXzHZDqUas4FAn@" + process.env.REACT_APP_MONGOEXPRESS);
              }}
            >
              Advanced browser
            </Nav.Link>
            <Nav.Link disabled>
              {searchOutput.length > 0 &&
                "Retrieved " + searchOutput.length + " results"}
            </Nav.Link>
            {searchOutput.length > 0 && (
              <ExportButton
                type={"all"}
                export={searchOutput.map((e) => {
                  return parseVersioning(e);
                })}
                downloadMode={downloadMode}
                changeDLMode={setDownloadMode}
              />
            )}
          </Nav>
          {isOpen ? (
            <Form inline className="align-items-center mr-2">
              <Form.Switch
                id="expressionMode"
                defaultChecked={expressionMode}
                onChange={() => {
                  setExpressionMode(!expressionMode);
                }}
                label={expressionMode ? "Expression mode" : "Field search"}
              />
              {expressionMode && (
                <OverlayTrigger placement="bottom" overlay={helpExpressionMode}>
                  <InfoIcon
                    className="ml-2"
                    style={{
                      color: "#007BFF",
                      height: "18px",
                      width: "18px",
                    }}
                  />
                </OverlayTrigger>
              )}
            </Form>
          ) : (
            <Form inline autoComplete="off" onSubmit={handleSubmit}>
              <FormControl
                type="text"
                placeholder="Search"
                className="mr-sm-2"
                onChange={handleSubmit}
              />
              <Button variant="outline-primary" type="submit">
                {loading ? (
                  <Spinner
                    as="span"
                    animation="border"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                  />
                ) : (
                  "Search"
                )}
              </Button>
            </Form>
          )}

          <Button
            variant="outline-primary"
            onClick={() => setIsOpen(!isOpen)}
            className="ml-1"
          >
            <NestedIcon
              style={{
                height: "18px",
                width: "18px",
              }}
            />
          </Button>
        </Navbar.Collapse>
      </Navbar>

      <Collapse in={isOpen}>
        <div style={{ backgroundColor: "#F8F9FA" }}>
          <AdvancedSearch
            toaster={props.toaster}
            setSearchOutput={setSearchOutput}
            expressionMode={expressionMode}
            setActivePage={setActivePage}
          />
        </div>
      </Collapse>
      <SearchResults elements={currentPageOutput()} />
      <Pagination className="mt-3 pb-3 justify-content-center">
        {searchOutput.length > 0 ? handlePages() : null}
      </Pagination>
    </TabPane>
  );
};

export default DatabaseTab;
