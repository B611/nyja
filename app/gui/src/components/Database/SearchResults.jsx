import { useState } from "react";
import {
  Accordion,
  Card,
  Media,
  Badge,
  Table,
  ListGroup,
  Tab,
  Nav,
  Tabs,
} from "react-bootstrap";
import { ReactComponent as SiteIcon } from "icons/site.svg";
import { ReactComponent as ArrowDownIcon } from "icons/arrowDown.svg";
import { ExportButton } from "components";
import { parseVersioning } from "./DatabaseTab";
import styled from "styled-components";

const ElemTitle = styled.h5`
  padding: 12px 12px 0 0;
`;

const StatusBadge = styled(Badge)`
  margin: 0 6px 6px 0;
`;

const Property = styled.th.attrs({ colSpan: 2 })`
  vertical-align: middle !important;
  align-content: middle !important;
`;

const Value = styled.td`
  vertical-align: middle !important;
  align-content: middle !important;
`;

const months = {
  0: "January",
  1: "February",
  2: "March",
  3: "April",
  4: "May",
  5: "June",
  6: "July",
  7: "August",
  8: "September",
  9: "October",
  10: "November",
  11: "December",
};

const SearchResults = (props) => {
  const [downloadMode, setDownloadMode] = useState("CSV");

  return (
    <Accordion className="mt-3">
      {props.elements.length > 0 ? (
        props.elements.map((element, idx) => {
          const entry = parseVersioning(element);
          return (
            <Card key={idx}>
              <Accordion.Toggle
                as={Media}
                eventKey={idx + 1}
                className="align-items-center"
              >
                {element.iconData ? (
                  <img
                    src={`data:image/${element.iconType};base64, ${element.iconData}`}
                    style={{
                      height: "42px",
                      width: "42px",
                      margin: "0 12px 0 12px",
                      alignSelf: "center",
                    }}
                    alt=""
                  />
                ) : (
                  <SiteIcon
                    style={{
                      height: "42px",
                      width: "42px",
                      margin: "0 12px 0 12px",
                      alignSelf: "center",
                    }}
                  />
                )}
                <Media.Body>
                  <ElemTitle>{element.title + " "}</ElemTitle>

                  <h4>
                    {element.online[element.online.length - 1].online ? (
                      <StatusBadge variant="success">Online</StatusBadge>
                    ) : (
                      <StatusBadge variant="danger">Offline</StatusBadge>
                    )}
                    {/* <StatusBadge variant="warning">Pornographic</StatusBadge>
                      <StatusBadge variant="dark">Market</StatusBadge>
                      <StatusBadge variant="primary">Indexer</StatusBadge> */}
                    {entry[entry.length - 1].captcha ? (
                      <StatusBadge variant="info">CAPTCHA</StatusBadge>
                    ) : null}
                    {entry[entry.length - 1].login ? (
                      <StatusBadge variant="info">Login</StatusBadge>
                    ) : null}
                    <StatusBadge variant="light">
                      {element.mirrors.length === 1
                        ? "1 Mirror"
                        : element.mirrors.length + " Mirrors"}
                    </StatusBadge>
                    {/* <StatusBadge variant="secondary">New</StatusBadge> */}
                  </h4>
                </Media.Body>
                <ExportButton
                  type={"single"}
                  export={entry}
                  downloadMode={downloadMode}
                  changeDLMode={setDownloadMode}
                />
              </Accordion.Toggle>
              <Accordion.Collapse eventKey={idx + 1}>
                <Tabs
                  defaultActiveKey={entry.length - 1}
                  className="mx-3 text-nowrap flex-nowrap"
                  style={
                    entry.length > 8
                      ? {
                          height: "50px",
                          overflowY: "hidden",
                          overflowX: "auto",
                          margin: "0 0 0 0",
                        }
                      : {
                          height: "40px",
                          margin: "0 0 0 0",
                        }
                  }
                >
                  {entry.map((e, idx) => {
                    return (
                      <Tab
                        key={idx}
                        eventKey={idx}
                        title={`${e.date.getDate()} ${
                          months[e.date.getMonth()]
                        } ${e.date.getFullYear()}`}
                        className="px-3 pt-1"
                      >
                        <Table responsive striped bordered hover>
                          <thead>
                            <tr>
                              <th colSpan="2" style={{ width: "10px" }}>
                                Property
                              </th>
                              <th>Value</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <Property>Title</Property>
                              <Value>{e.title}</Value>
                            </tr>
                            <tr>
                              <Property>CAPTCHA Protection</Property>
                              <Value>
                                {e.captcha ? (
                                  <h4>
                                    <Badge variant="success">Yes</Badge>
                                  </h4>
                                ) : (
                                  <h4>
                                    <Badge variant="danger">No</Badge>
                                  </h4>
                                )}
                              </Value>
                            </tr>
                            <tr>
                              <Property>Login System</Property>
                              <Value>
                                {e.login ? (
                                  <h4>
                                    <Badge variant="success">Yes</Badge>
                                  </h4>
                                ) : (
                                  <h4>
                                    <Badge variant="danger">No</Badge>
                                  </h4>
                                )}
                              </Value>
                            </tr>
                            <tr>
                              <Property>Cryptocurrency in use</Property>
                              <Value>
                                {e.crypto.length !== 0 ? (
                                  <h5>
                                    {e.crypto.map((elem, key) => {
                                      return (
                                        <Badge
                                          variant="dark"
                                          className="mr-1"
                                          key={idx + "crypto" + key}
                                        >
                                          {elem}
                                        </Badge>
                                      );
                                    })}
                                  </h5>
                                ) : (
                                  "None"
                                )}
                              </Value>
                            </tr>
                            <tr>
                              <th
                                rowSpan="2"
                                style={{
                                  verticalAlign: "middle",
                                  alignContent: "middle",
                                }}
                              >
                                Products
                              </th>
                              <th>Drugs</th>
                              <Value>
                                {e.products.drugs.length !== 0 ? (
                                  <h5>
                                    {e.products.drugs.map((elem, key) => {
                                      return (
                                        <Badge
                                          variant="dark"
                                          className="mr-1 text-capitalize"
                                          key={idx + "prod" + key}
                                        >
                                          {elem}
                                        </Badge>
                                      );
                                    })}
                                  </h5>
                                ) : (
                                  "None"
                                )}
                              </Value>
                            </tr>
                            <tr>
                              <th>Weapons</th>
                              <Value>
                                {e.products.weapons.length !== 0 ? (
                                  <h5>
                                    {e.products.weapons.map((elem, key) => {
                                      return (
                                        <Badge
                                          variant="dark"
                                          className="mr-1 text-capitalize"
                                          key={idx + "weap" + key}
                                        >
                                          {elem}
                                        </Badge>
                                      );
                                    })}
                                  </h5>
                                ) : (
                                  "None"
                                )}
                              </Value>
                            </tr>
                            <tr>
                              <Property>Scan time</Property>
                              <Value>{e.date.toString()}</Value>
                            </tr>
                            <tr>
                              <Property>Mirrors</Property>
                              <Value>
                                {e.mirrors.length !== 0
                                  ? e.mirrors.map((elem, key) => {
                                      return (
                                        <Accordion key={idx + "card" + key}>
                                          <Card>
                                            <Accordion.Toggle
                                              as={Card.Header}
                                              eventKey={idx + 1}
                                              className="d-flex justify-content-between"
                                            >
                                              {elem.address}
                                              <ArrowDownIcon
                                                style={{
                                                  height: "24px",
                                                  width: "24px",
                                                }}
                                              />
                                            </Accordion.Toggle>
                                            <Accordion.Collapse
                                              eventKey={idx + 1}
                                            >
                                              <Card.Body>
                                                <h5>
                                                  Is indexed on :<br></br>
                                                </h5>
                                                <ListGroup variant="flush"></ListGroup>
                                                {elem.indexers.map(
                                                  (elem, key) => {
                                                    return (
                                                      <ListGroup.Item
                                                        key={
                                                          idx + "indexer" + key
                                                        }
                                                      >
                                                        <Card.Link>
                                                          {elem}
                                                        </Card.Link>
                                                      </ListGroup.Item>
                                                    );
                                                  }
                                                )}
                                              </Card.Body>
                                            </Accordion.Collapse>
                                          </Card>
                                        </Accordion>
                                      );
                                    })
                                  : "None"}
                              </Value>
                            </tr>
                          </tbody>
                        </Table>
                      </Tab>
                    );
                  })}
                  {/* </Tab.Content> */}
                </Tabs>
                {/* <Table responsive striped bordered hover>
                    <thead>
                      <tr>
                        <th colSpan="2" style={{ width: "10px" }}>
                          Property
                        </th>
                        <th>Value</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <Property>Title</Property>
                        <Value>{element.title}</Value>
                      </tr>
                      <tr>
                        <Property>CAPTCHA Protection</Property>
                        <Value>
                          {element.captcha ? (
                            <h4>
                              <Badge variant="success">Yes</Badge>
                            </h4>
                          ) : (
                            <h4>
                              <Badge variant="danger">No</Badge>
                            </h4>
                          )}
                        </Value>
                      </tr>
                      <tr>
                        <Property>Login System</Property>
                        <Value>
                          {element.login ? (
                            <h4>
                              <Badge variant="success">Yes</Badge>
                            </h4>
                          ) : (
                            <h4>
                              <Badge variant="danger">No</Badge>
                            </h4>
                          )}
                        </Value>
                      </tr>
                      <tr>
                        <Property>Cryptocurrency in use</Property>
                        <Value>
                          {element.crypto.length !== 0 ? (
                            <h5>
                              {element.crypto.map((elem, key) => {
                                return (
                                  <Badge
                                    variant="dark"
                                    className="mr-1"
                                    key={idx + "crypto" + key}
                                  >
                                    {elem}
                                  </Badge>
                                );
                              })}
                            </h5>
                          ) : (
                            "None"
                          )}
                        </Value>
                      </tr>
                      <tr>
                        <th
                          rowSpan="2"
                          style={{
                            verticalAlign: "middle",
                            alignContent: "middle",
                          }}
                        >
                          Products
                        </th>
                        <th>Drugs</th>
                        <Value>
                          {element.products.drugs.length !== 0 ? (
                            <h5>
                              {element.products.drugs.map((elem, key) => {
                                return (
                                  <Badge
                                    variant="dark"
                                    className="mr-1 text-capitalize"
                                    key={idx + "prod" + key}
                                  >
                                    {elem}
                                  </Badge>
                                );
                              })}
                            </h5>
                          ) : (
                            "None"
                          )}
                        </Value>
                      </tr>
                      <tr>
                        <th>Weapons</th>
                        <Value>
                          {element.products.weapons.length !== 0 ? (
                            <h5>
                              {element.products.weapons.map((elem, key) => {
                                return (
                                  <Badge
                                    variant="dark"
                                    className="mr-1 text-capitalize"
                                    key={idx + "weap" + key}
                                  >
                                    {elem}
                                  </Badge>
                                );
                              })}
                            </h5>
                          ) : (
                            "None"
                          )}
                        </Value>
                      </tr>
                      <tr>
                        <Property>Mirrors</Property>
                        <Value>
                          {element.mirrors.length !== 0
                            ? element.mirrors.map((elem, key) => {
                                return (
                                  <Accordion key={idx + "card" + key}>
                                    <Card>
                                      <Accordion.Toggle
                                        as={Card.Header}
                                        eventKey={idx + 1}
                                        className="d-flex justify-content-between"
                                      >
                                        {elem.address}
                                        <ArrowDownIcon
                                          style={{
                                            height: "24px",
                                            width: "24px",
                                          }}
                                        />
                                      </Accordion.Toggle>
                                      <Accordion.Collapse eventKey={idx + 1}>
                                        <Card.Body>
                                          <h5>
                                            Is indexed on :<br></br>
                                          </h5>
                                          <ListGroup variant="flush"></ListGroup>
                                          {elem.indexers.map((elem, key) => {
                                            return (
                                              <ListGroup.Item
                                                key={idx + "indexer" + key}
                                              >
                                                <Card.Link>{elem}</Card.Link>
                                              </ListGroup.Item>
                                            );
                                          })}
                                        </Card.Body>
                                      </Accordion.Collapse>
                                    </Card>
                                  </Accordion>
                                );
                              })
                            : "None"}
                        </Value>
                      </tr>
                    </tbody>
                  </Table> */}
              </Accordion.Collapse>
            </Card>
          );
        })
      ) : (
        <Nav.Link disabled>Search for onions in the database</Nav.Link>
      )}
    </Accordion>
  );
};

export default SearchResults;
