import { TabPane, Card } from "react-bootstrap";

const StatsTab = () => {
  return (
    <TabPane eventKey="#stats">
      <Card style={{ width: "30rem" }}>
        <Card.Body className="align-content-center">
          <Card.Title>Statistics</Card.Title>
          The statistics page is still in development for now. ¯\_(ツ)_/¯
        </Card.Body>
      </Card>
    </TabPane>
  );
};

export default StatsTab;
