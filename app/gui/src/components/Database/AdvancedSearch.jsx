import {
  Button,
  Spinner,
  Form,
  FormControl,
  FormGroup,
  InputGroup,
} from "react-bootstrap";
import { ReactComponent as SearchIcon } from "icons/search.svg";
import { run_task } from "components";
import { useState } from "react";

const trueFalseTable = {
  TITLE: false,
  LOGIN: true,
  CAPTCHA: true,
  CRYPTO: false,
  PRODUCTS: false,
  HTML: false,
  ADDRESSES: false,
  INDEXERS: false,
  ONLINE: true,
};

const AdvancedSearch = (props) => {
  const [loading, setLoading] = useState(false);
  const [validity, setValidity] = useState(false);
  const [isTrueFalse, setIsTrueFalse] = useState(false);
  const { toaster, setSearchOutput, expressionMode, setActivePage } = props;

  const checkValid = async (query, check) => {
    const response = await run_task({
      command: "nested",
      query: query,
    }).catch(() => {
      toaster("Error", "An error occured when trying to launch a search.");
      setLoading(false);
    });
    if (response && !(response instanceof Error)) {
      if (response === "Nested expression not recognised") {
        setValidity(false);
        setLoading(false);
      } else {
        setValidity(true);
        setLoading(false);
        if (!check) {
          setSearchOutput(response);
          setActivePage(1);
        }
      }
    } else if (response === undefined || response instanceof Error) {
      toaster("Error", "An error occured when trying to search for " + query);
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    setLoading(true);
    // Handle onSubmit
    if (event.target.length > 0) {
      event.preventDefault();
      let field = event.target[0].value;
      let value = event.target[1].value;
      if (!value) checkValid("ALL");
      checkValid(field + " " + value);
      // Handle onChange
    }
  };

  const checkValidExpression = (event) => {
    if (event.target.value) {
      event.preventDefault();
      checkValid(event.target.value, true);
    }
  };

  const searchNested = (event) => {
    setLoading(true);
    event.preventDefault();
    checkValid(event.target[0].value);
  };

  return expressionMode ? (
    <Form
      noValidate
      validated={validity}
      autoComplete="off"
      onSubmit={searchNested}
      className="mx-3 pb-1 pt-1"
    >
      <FormGroup className="align-self-center">
        <InputGroup>
          <FormControl
            type="text"
            isInvalid={!validity}
            placeholder="Search expression"
            className="mr-sm-2"
            onChange={checkValidExpression}
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
              <SearchIcon
                style={{
                  height: "18px",
                  width: "18px",
                }}
              />
            )}
          </Button>
        </InputGroup>
      </FormGroup>
    </Form>
  ) : (
    <Form autoComplete="off" onSubmit={handleSubmit} className="mx-3 pb-3 pt-1">
      <InputGroup>
        <FormControl
          as="select"
          className="mr-sm-2"
          onChange={(e) => setIsTrueFalse(trueFalseTable[e.target.value])}
        >
          <option>TITLE</option>
          <option>LOGIN</option>
          <option>CAPTCHA</option>
          <option>CRYPTO</option>
          <option>PRODUCTS</option>
          <option>HTML</option>
          <option>ADDRESSES</option>
          <option>INDEXERS</option>
          <option>ONLINE</option>
        </FormControl>
        {isTrueFalse ? (
          <FormControl as="select" className="mr-sm-2">
            <option value="true">Yes</option>
            <option value="false">No</option>
          </FormControl>
        ) : (
          <FormControl type="text" placeholder="Keyword" className="mr-sm-2" />
        )}

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
      </InputGroup>
    </Form>
  );
};

export default AdvancedSearch;
