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
} from "react-bootstrap";
import { run_task, FileInput } from "components";

const Indexer = (props) => {
  const [crawlOutput, setCrawlOutput] = useState([]);

  const handleTask = async (url, save, file = "") => {
    const data = new FormData();
    data.append("file", file);
    data.append("command", "crawl");
    data.append("save", save ? save : "");
    const response = await run_task(
      file
        ? data
        : {
            command: "crawl",
            address: url,
            save: save,
          }
    ).catch((err) => {
      props.toaster("Error", "An error occured when trying to launch a crawl.");
    });
    if (response) {
      const newOutput = crawlOutput;
      if (response instanceof Object) {
        newOutput.push({ site: url, output: JSON.stringify(response) });
      } else {
        newOutput.push({ site: url, output: response });
      }
      setCrawlOutput(newOutput);
      props.toaster("Crawler", "Crawling of indexer " + url + " finished.");
    } else if (response === undefined) {
      props.toaster("Error", "An error occured when trying to launch a crawl.");
    } else {
      props.toaster("Info", "Crawl of " + url + " returned with no output");
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
      props.toaster("Crawler", "Launched crawling of indexer " + url);
      handleTask(url, save);
    } else if (fileList.length > 0) {
      handleTask("", save, fileList[0]);
      props.toaster(
        "Crawler",
        "Launched indexer crawling for " + fileList[0].name
      );
    }
  };

  return (
    <TabPane eventKey="#indexers">
      <Card.Body>
        <Card.Title>Crawl indexers to find onion sites</Card.Title>
        <Form onSubmit={handleSubmit} className="mt-3" autoComplete="off">
          <Row>
            <Form.Group as={Col}>
              <InputGroup className="mb-3">
                <InputGroup.Prepend>
                  <InputGroup.Text id="addon-crawl">
                    Indexer URL
                  </InputGroup.Text>
                </InputGroup.Prepend>
                <FormControl placeholder="http://" id="placeholder-crawl" />
              </InputGroup>
            </Form.Group>
            <FileInput />
          </Row>
          <Row className="ml-1">
            <Form.Group as={Col}>
              <Form.Check
                id="save-db-crawl"
                type="switch"
                defaultChecked={true}
                className="mb-3"
                label="Save onions to database"
              />
            </Form.Group>
          </Row>
          <Row className="justify-content-end mr-1">
            <Button style={{ width: "80px" }} type="submit">
              Run
            </Button>
          </Row>
        </Form>
        <Accordion className="mt-3">
          {crawlOutput
            ? crawlOutput.map((element, idx) => {
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
    </TabPane>
  );
};

export default Indexer;
