import { ListGroup } from "react-bootstrap";
import { ReactComponent as SpiderIcon } from "icons/spider.svg";
import { ReactComponent as DatabaseIcon } from "icons/database.svg";
import { ReactComponent as InsightIcon } from "icons/trend.svg";
import styled from "styled-components";

const ListItem = styled(ListGroup.Item)`
  text-align: center;
  &[aria-selected="true"] {
    background-color: lightgrey;
    border-color: lightgrey;
    color: black;
  }
`;

const Menu = () => {
  return (
    <ListGroup style={{ fontSize: "1.2rem" }}>
      <ListItem action href="#crawl">
        Crawling
        <SpiderIcon
          style={{ height: "42px", width: "42px", paddingLeft: "12px" }}
        />
      </ListItem>
      <ListItem action href="#browser">
        Database
        <DatabaseIcon
          style={{ height: "42px", width: "42px", paddingLeft: "12px" }}
        />
      </ListItem>
      <ListItem action href="#stats">
        Statistics
        <InsightIcon
          style={{ height: "42px", width: "42px", paddingLeft: "12px" }}
        />
      </ListItem>
    </ListGroup>
  );
};

export default Menu;
