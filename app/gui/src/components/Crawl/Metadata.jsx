import { useState } from "react";
import {
  TabPane,
  Card,
  Button,
  InputGroup,
  FormControl,
  Form,
  Col,
  Row,
  Accordion,
  Modal,
} from "react-bootstrap";
import { run_task, FileInput } from "components";

const Metadata = (props) => {
  const [metaOutput, setMetaOutput] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [nbOnions, setNbOnions] = useState(0);

  const handleTask = async (url, save, file = "") => {
    const data = new FormData();
    data.append("file", file);
    data.append("command", "metadata");
    data.append("save", save ? save : "");
    const response = await run_task(
      file
        ? data
        : {
            command: "metadata",
            address: url,
            save: save,
          }
    ).catch((err) => {
      props.toaster(
        "Error",
        "An error occured when trying to launch metadata harvesting."
      );
    });
    if (response && !Array.isArray(response)) {
      const newOutput = metaOutput;
      newOutput.push({
        site: url,
        output: JSON.stringify(response, null, 2),
      });
      setMetaOutput(newOutput);
      props.toaster(
        "Metadata",
        "Metadata harvesting of indexer " + url + " finished."
      );
    } else if (response === undefined) {
      props.toaster(
        "Error",
        "An error occured when trying to launch metadata harvesting."
      );
    } else {
      props.toaster(
        "Info",
        "Metadata harvesting of " + url + " returned with no output"
      );
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    let url = event.target[0].value;
    const fileList = event.target[1].files;
    const save = event.target[2].checked;
    if (url) {
      if (!url.startsWith("http")) {
        url = "http://" + url;
      }
      props.toaster("Metadata", "Launched metadata scraping of " + url);
      handleTask(url, save);
    } else if (fileList.length > 0) {
      handleTask("", save, fileList[0]);
      props.toaster(
        "Metadata",
        "Launched metadata scraping for " + fileList[0].name
      );
    }
  };

  const getOnionsInDB = async (query) => {
    const response = await run_task({
      command: "uncrawled",
    }).catch(() => {
      props.toaster(
        "Error",
        "An error occured when trying to launch a search."
      );
    });
    if (response && !(response instanceof Error)) {
      setNbOnions(response);
    } else if (response === undefined || response instanceof Error) {
      props.toaster(
        "Error",
        "An error occured when trying to search for " + query
      );
    }
  };

  const metadataAll = (event) => {
    props.toaster("Metadata", "Launched metadata scraping of all saved sites");
    handleTask("", true);
  };

  return (
    <TabPane eventKey="#meta">
      <Card.Body>
        <Card.Title>Scrape metadata from onion sites</Card.Title>
        <Form onSubmit={handleSubmit} className="mt-3" autoComplete="off">
          <Row>
            <Form.Group as={Col}>
              <InputGroup className="mb-3">
                <InputGroup.Prepend>
                  <InputGroup.Text id="addon-meta">Onion URL</InputGroup.Text>
                </InputGroup.Prepend>
                <FormControl placeholder="http://" id="placeholder-meta" />
              </InputGroup>
            </Form.Group>
            <FileInput />
          </Row>
          <Row className="ml-1">
            <Form.Group as={Col}>
              <Form.Check
                id="save-db-meta"
                type="switch"
                defaultChecked={true}
                className="mb-3"
                label="Save metadata to database"
              />
            </Form.Group>
          </Row>
          <Row className="justify-content-end mr-1">
            <Button
              className="mr-1"
              variant="success"
              onClick={() => getOnionsInDB("").then(() => setShowModal(true))}
            >
              Run on all saved
            </Button>
            <Button style={{ width: "80px" }} type="submit">
              Run
            </Button>
          </Row>
        </Form>
        <Accordion className="mt-3">
          {metaOutput
            ? metaOutput.map((element, idx) => {
                return (
                  <Card key={idx}>
                    <Accordion.Toggle as={Card.Header} eventKey={idx + 1}>
                      Output from {element.site}
                    </Accordion.Toggle>
                    <Accordion.Collapse eventKey={idx + 1}>
                      <Card.Body style={{ whiteSpace: "pre-wrap" }}>
                        {element.output}
                      </Card.Body>
                    </Accordion.Collapse>
                  </Card>
                );
              })
            : null}
        </Accordion>
      </Card.Body>
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Crawl all database</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          There are <strong>{nbOnions}</strong> onion links saved in the
          database.
          <br />
          Do you really want to harvest metadata on all of them ?<br />
          This might take a long time.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
          <Button
            variant="primary"
            onClick={() => {
              setShowModal(false);
              metadataAll();
            }}
          >
            Launch metadata harvesting
          </Button>
        </Modal.Footer>
      </Modal>
    </TabPane>
  );
};

export default Metadata;
