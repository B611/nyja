import { TabPane, TabContainer, TabContent, Card, Nav } from "react-bootstrap";
import { Indexer, Metadata, Misc } from "components";
import { ReactComponent as SettingIcon } from "icons/settings.svg";

const CrawlTab = (props) => {
  return (
    <TabPane eventKey="#crawl">
      <TabContainer defaultActiveKey="#indexers">
        <Card>
          <Card.Header>
            <Nav variant="tabs">
              <Nav.Item>
                <Nav.Link eventKey="#indexers">Indexers</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="#meta">Metadata</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="#misc">
                  <SettingIcon
                    style={{
                      height: "18px",
                      width: "18px",
                    }}
                  />
                </Nav.Link>
              </Nav.Item>
            </Nav>
          </Card.Header>
          <TabContent>
            <Indexer toaster={props.toaster} />
            <Metadata toaster={props.toaster} />
            <Misc
              populateVisible={props.populateVisible}
              schedulerVisible={props.schedulerVisible}
            />
          </TabContent>
        </Card>
      </TabContainer>
    </TabPane>
  );
};

export default CrawlTab;
