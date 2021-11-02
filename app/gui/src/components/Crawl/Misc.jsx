import { TabPane, Card, Row } from "react-bootstrap";
import { ReactComponent as DatabaseIcon } from "icons/database.svg";
import { ReactComponent as ScheduleIcon } from "icons/timer.svg";

const Misc = (props) => {
  return (
    <TabPane eventKey="#misc">
      <Card.Body>
        <Card.Title>Miscellaneous commands</Card.Title>
        <Row>
          <Card
            style={{ width: "30rem" }}
            onClick={() => props.populateVisible(true)}
            className="ml-3"
          >
            <Card.Body className="align-content-center">
              <Card.Title>
                <DatabaseIcon
                  className="mr-2"
                  style={{
                    height: "18px",
                    width: "18px",
                    margin: "0 0 3px 0px",
                  }}
                />
                Populate database
              </Card.Title>
              Populate database with default Nyja indexers and crawl metadata on
              all retrieved onions.
            </Card.Body>
          </Card>
          <Card
            style={{ width: "30rem" }}
            onClick={() => props.schedulerVisible(true)}
            className="ml-3"
          >
            <Card.Body className="align-content-center">
              <Card.Title>
                <ScheduleIcon
                  className="mr-2"
                  style={{
                    height: "18px",
                    width: "18px",
                    margin: "0 0 3px 0px",
                  }}
                />
                Task scheduler
              </Card.Title>
              Schedule tasks to continuously monitor changes on your onions.
            </Card.Body>
          </Card>
        </Row>
      </Card.Body>
    </TabPane>
  );
};

export default Misc;
