import { Modal, Button, Form, Row, Col } from "react-bootstrap";
import { ReactComponent as TimeIcon } from "icons/timer.svg";
import { ReactComponent as DeleteIcon } from "icons/delete.svg";
import { useState, useEffect } from "react";
import { get_schedule, set_schedule } from "components";
import "./SchedulerModal.css";

const days_list = {
  mon: <option value="mon">Every Monday</option>,
  tue: <option value="tue">Every Tuesday</option>,
  wed: <option value="wed">Every Wednesday</option>,
  thu: <option value="thu">Every Thursday</option>,
  fri: <option value="fri">Every Friday</option>,
  sat: <option value="sat">Every Saturday</option>,
  sun: <option value="sun">Every Sunday</option>,
  "*": <option value="*">Everyday</option>,
};

const SchedulerModal = (props) => {
  const [taskList, setTaskList] = useState([]);
  const { visible, setVisible, showToast } = props;

  const cronToTaskList = (cronList) => {
    console.log(cronList);
    return cronList.map((elem) => {
      const task = elem.split(" ");
      const minute = task[0];
      const hour = task[1];
      const day = task[4];
      const command = task[7].replace("\n", "");
      const address = task[8] ? task[8].replace("\n", "") : "";
      return {
        command: command,
        address: address,
        day: day,
        hour: hour,
        minute: minute,
      };
    });
  };

  const taskToCronTab = (taskList) => {
    const newCronTab = ["*/1 * * * * crontab /app/cron_schedule"];
    newCronTab.push(
      ...taskList.map((elem) => {
        return `${elem.minute || 0} ${elem.hour} * * ${
          elem.day
        } python3 /app/scheduler_wrapper.py ${elem.command}${
          elem.address ? " " + elem.address : ""
        }`;
      })
    );
    console.log(newCronTab.join("\n"));
    return newCronTab.join("\n");
  };

  const addTask = (e) => {
    e.preventDefault();
    const command = e.target[0].value;
    const address = e.target[1].value;
    if ((command === "crawl" || command === "populate") && !address) return;
    const day = e.target[2].value;
    const hour = e.target[3].value;
    const newList = [...taskList];
    if (command === "populate") {
      newList.push({
        command: "crawl",
        address: address,
        day: day,
        hour: hour,
        minute: "0",
      });
      newList.push({
        command: "metadata",
        address: "",
        day: day,
        hour: hour,
        minute: "1",
      });
    } else {
      newList.push({
        command: command,
        address: address,
        day: day,
        hour: hour,
        minute: "0",
      });
    }
    setTaskList(newList);
    console.log(taskList);
  };

  const sendSchedule = async (cronTab) => {
    const response = await set_schedule(cronTab).catch(() => {
      showToast("Scheduler", "Error when scheduling tasks");
    });
    if (response && !(response instanceof Error)) {
      showToast("Scheduler", "Scheduled tasks saved successfully !");
    } else if (response === undefined || response instanceof Error) {
      showToast("Scheduler", "Error when scheduling tasks");
    }
  };

  useEffect(
    () =>
      (() => async (showToast) => {
        if (!visible) {
          const response = await get_schedule().catch(() => {
            showToast(
              "Error",
              "An error occured when trying to retrieve scheduled tasks."
            );
          });
          if (response && !(response instanceof Error)) {
            const newList = cronToTaskList(
              response.data.filter((e, idx) => idx !== 0 && e !== " \n")
            );
            setTaskList(newList);
          } else if (response === undefined || response instanceof Error) {
            showToast(
              "Error",
              "An error occured when trying to retrieve scheduled tasks."
            );
          }
        }
      })(),
    [visible]
  );

  return (
    <Modal
      id="scheduler-modal"
      dialogClassName="modal-90w"
      show={visible}
      onHide={() => props.setVisible(false)}
      onSubmit={addTask}
      autoComplete="off"
    >
      <Modal.Header closeButton>
        <Modal.Title>
          <TimeIcon
            className="mr-3"
            style={{
              height: "22px",
              width: "22px",
              margin: "0 0 4px 0",
            }}
          />
          Task scheduler
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <h5>New task</h5>
        <Form>
          <Row>
            <Form.Group as={Col}>
              <Form.Control as="select" className="my-1" id="cmdSelect" custom>
                <option value="crawl">Indexer crawling</option>
                <option value="metadata">Metadata harvesting</option>
                <option value="populate">
                  Indexer crawling + Metadata on retrieved
                </option>
              </Form.Control>
            </Form.Group>
            <Form.Group as={Col}>
              <Form.Control
                className="my-1"
                id="inpSelect"
                placeholder="of http://"
                autoComplete="off"
              />
            </Form.Group>
            <Form.Group as={Col}>
              <Form.Control as="select" className="my-1" id="daySelect" custom>
                <option value="mon">Every Monday</option>
                <option value="tue">Every Tuesday</option>
                <option value="wed">Every Wednesday</option>
                <option value="thu">Every Thursday</option>
                <option value="fri">Every Friday</option>
                <option value="sat">Every Saturday</option>
                <option value="sun">Every Sunday</option>
                <option value="*">Everyday</option>
              </Form.Control>
            </Form.Group>
            <Form.Group as={Col}>
              <Form.Control as="select" className="my-1" id="hourSelect" custom>
                {[...Array(24).keys()].map((item, idx) => {
                  const hour = String(item).padStart(2, "0") + ":00";
                  return (
                    <option value={item} key={idx}>
                      at {hour}
                    </option>
                  );
                })}
              </Form.Control>
            </Form.Group>
            <Form.Group as={Col} lg="auto">
              <Button type="submit" className="my-1" variant="outline-primary">
                Add
              </Button>
            </Form.Group>
          </Row>
        </Form>
        <hr />
        <h5>Existing tasks</h5>
        {taskList.map((elem, idx) => {
          return (
            <Form key={idx}>
              <Row>
                <Form.Group as={Col}>
                  <Form.Control
                    as="select"
                    className="my-1"
                    id="cmdSelect"
                    disabled
                    custom
                  >
                    {elem.command === "crawl" ? (
                      <option value="crawl">Indexer crawling</option>
                    ) : (
                      <option value="metadata">Metadata harvesting</option>
                    )}
                  </Form.Control>
                </Form.Group>
                <Form.Group as={Col}>
                  <Form.Control
                    className="my-1"
                    id="inpSelect"
                    value={
                      elem.address
                        ? elem.address.replaceAll('"', "")
                        : elem.command === "crawl"
                        ? ""
                        : "on all saved onions"
                    }
                    disabled
                  />
                </Form.Group>
                <Form.Group as={Col}>
                  <Form.Control
                    as="select"
                    className="my-1"
                    id="daySelect"
                    disabled
                    custom
                  >
                    {days_list[elem.day]}
                  </Form.Control>
                </Form.Group>
                <Form.Group as={Col}>
                  <Form.Control
                    as="select"
                    className="my-1"
                    id="hourSelect"
                    disabled
                    custom
                  >
                    <option value={elem.hour}>
                      {" "}
                      at{" "}
                      {elem.hour.padStart(2, "0") +
                        ":" +
                        elem.minute.padStart(2, "0")}
                    </option>
                    ;
                  </Form.Control>
                </Form.Group>
                <Form.Group as={Col} lg="auto">
                  <Button
                    className="my-1"
                    variant="outline-danger"
                    onClick={() => {
                      const newList = [...taskList];
                      newList.splice(idx, 1);
                      setTaskList(newList);
                    }}
                  >
                    <DeleteIcon
                      style={{
                        height: "20px",
                        width: "20px",
                      }}
                    />
                  </Button>
                </Form.Group>
              </Row>
            </Form>
          );
        })}
      </Modal.Body>
      <Modal.Footer>
        <Button
          variant="secondary"
          onClick={() => {
            setVisible(false);
          }}
        >
          Close
        </Button>
        <Button
          variant="primary"
          onClick={() => {
            sendSchedule({ new_config: taskToCronTab(taskList) });
            setVisible(false);
          }}
        >
          Confirm tasks
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default SchedulerModal;
