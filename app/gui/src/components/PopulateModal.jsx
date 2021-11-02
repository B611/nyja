import { Modal, Button, Alert } from "react-bootstrap";
import { ReactComponent as TimeIcon } from "icons/timer.svg";
import { run_task } from "components";

const PopulateModal = (props) => {
  const launchPopulate = async () => {
    const response = await run_task({
      command: "populate",
      indexer: "/app/user_dir/indexers",
    }).catch(() => {
      props.showToast(
        "Error",
        "An error occured when trying to launch a populate command."
      );
    });
    if (response && !(response instanceof Error)) {
    } else if (response === undefined || response instanceof Error) {
      props.showToast(
        "Error",
        "An error occured when trying to launch a populate command."
      );
    }
  };

  return (
    <Modal
      size="lg"
      show={props.populateModalVisible}
      onHide={() => props.setPopulateModalVisible(false)}
    >
      <Modal.Header closeButton>
        <Modal.Title>First launch</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        Do you want to populate the database with default Nyja indexers ?
        <br />
        This will automatically crawl indexers and harvest metadata from all
        retrieved onion links.
        <br />
        <Alert className={"mt-3"} variant={"warning"}>
          <TimeIcon
            className="mr-3"
            style={{
              height: "18px",
              width: "18px",
              margin: "0 0 0 8px",
            }}
          />
          This might take a very long time depending on your internet speed.
        </Alert>
      </Modal.Body>
      <Modal.Footer>
        <Button
          variant="outline-secondary"
          onClick={() => {
            localStorage.setItem("populated", true);
            props.setPopulateModalVisible(false);
          }}
        >
          Don't ask me again
        </Button>
        <Button
          variant="secondary"
          onClick={() => {
            localStorage.clear();
            props.setPopulateModalVisible(false);
          }}
        >
          Maybe later
        </Button>
        <Button
          variant="primary"
          onClick={() => {
            launchPopulate();
            localStorage.setItem("populated", true);
            props.setPopulateModalVisible(false);
            props.showToast(
              "Populate",
              "Crawling and metadata harvesting process started. This might take a long time to complete."
            );
          }}
        >
          Launch populate
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default PopulateModal;
