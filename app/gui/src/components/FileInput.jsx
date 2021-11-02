import { useState } from "react";
import { Form, Col } from "react-bootstrap";

const FileInput = (props) => {
  const [fileName, setFileName] = useState("");
  const [validity, setValidity] = useState(false);
  const [error, setError] = useState(false);

  const checkValidity = (file) => {
    setError(false);
    setValidity(false);
    if (file.type === "" || file.type.includes("text")) {
      setValidity(true);
    } else {
      setError(true);
    }
  };

  return (
    <Form.Group as={Col}>
      <Form.File className="mb-3" id="idx-file-crawl" custom>
        <Form.File.Input
          isValid={validity}
          isInvalid={error}
          onChange={(e) => {
            setFileName(e.target.files[0].name);
            checkValidity(e.target.files[0]);
          }}
        />
        <Form.File.Label>Or file input</Form.File.Label>
        <Form.Control.Feedback type="valid">
          File {fileName} uploaded !
        </Form.Control.Feedback>
        <Form.Control.Feedback type="invalid">
          File format appears to be invalid. Please upload a list of onions such
          as: <br />
          abc.onion
          <br />
          xyz.onion
        </Form.Control.Feedback>
      </Form.File>
    </Form.Group>
  );
};

export default FileInput;
