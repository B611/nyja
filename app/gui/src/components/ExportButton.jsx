import {
  Button,
  OverlayTrigger,
  Dropdown,
  ButtonGroup,
  NavDropdown,
} from "react-bootstrap";
import { ReactComponent as DownloadIcon } from "icons/download.svg";

const ExportButton = (props) => {
  const { downloadMode, changeDLMode, type } = props;

  const chooseDownloadModeSingle = (arrowProps, ...props) => {
    return (
      <div>
        <Dropdown.Menu variant="light">
          <Dropdown.Header>Export format</Dropdown.Header>
          <Dropdown.Item onClick={() => changeDLMode("CSV")}>CSV</Dropdown.Item>
          <Dropdown.Item onClick={() => changeDLMode("JSON")}>
            JSON
          </Dropdown.Item>
        </Dropdown.Menu>
      </div>
    );
  };

  const cleanThis = (entry) => {
    let setEntry = [...new Set(entry)].filter((x) => x !== null);
    if (entry.length === 0) return "";
    setEntry = setEntry.map((e) => {
      return e.trim();
    });
    return setEntry.toString().replaceAll(",", ";");
  };

  const convertToCSV = (objectArray) => {
    let csv = "";
    csv += "address,indexers,title,crypto,drugs,weapons,login,captcha,date\r\n";
    objectArray.map((entry) => {
      if (Array.isArray(entry)) {
        entry = entry[0];
      }
      return entry.mirrors.map((mirrorEntry) => {
        csv +=
          mirrorEntry.address + "," + cleanThis(mirrorEntry.indexers) + ",";
        csv +=
          entry.title.trim().replaceAll(",", "-") +
          "," +
          cleanThis(entry.crypto) +
          "," +
          cleanThis(entry.products.drugs) +
          "," +
          cleanThis(entry.products.weapons) +
          "," +
          entry.login +
          "," +
          entry.captcha +
          "," +
          entry.date;
        csv += "\r\n";
        return csv;
      });
    });
    return csv;
  };

  const downloadFormatter = (elem) => {
    if (!elem || elem.length === 0 || elem[0].length === 0) return;
    switch (downloadMode) {
      case "CSV":
        return (
          "data:text/plain;base64," +
          btoa(unescape(encodeURIComponent(convertToCSV(elem))))
        );
      default:
        return (
          "data:text/plain;base64," +
          btoa(unescape(encodeURIComponent(JSON.stringify(elem))))
        );
    }
  };

  return (
    <Dropdown
      as={ButtonGroup}
      className="mr-3"
      onClick={(e) => {
        e.stopPropagation();
      }}
    >
      <Button
        variant="light"
        onClick={(e) => {
          e.stopPropagation();
        }}
        href={downloadFormatter(props.export)}
        download={
          type === "single"
            ? (props.export[0].title ? props.export[0].title.toString() : "") +
              "." +
              downloadMode.toLowerCase()
            : "metadata." + downloadMode.toLowerCase()
        }
        className="align-items-center"
      >
        {downloadMode}
        <DownloadIcon
          style={{
            height: "18px",
            width: "18px",
            margin: "0 0 0 8px",
          }}
        />
      </Button>

      {type === "single" ? (
        <OverlayTrigger
          placement="right"
          trigger="focus"
          overlay={chooseDownloadModeSingle}
        >
          <Dropdown.Toggle split variant="light" />
        </OverlayTrigger>
      ) : (
        <NavDropdown variant="light" id="nav-dropdown">
          <NavDropdown.Item onClick={() => changeDLMode("CSV")}>
            CSV
          </NavDropdown.Item>
          <NavDropdown.Item onClick={() => changeDLMode("JSON")}>
            JSON
          </NavDropdown.Item>
        </NavDropdown>
      )}
    </Dropdown>
  );
};

export default ExportButton;
