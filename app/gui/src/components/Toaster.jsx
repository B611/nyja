import { Toast } from "react-bootstrap";
import { useState } from "react";
import styled from "styled-components";
import { ReactComponent as SpiderIcon } from "icons/spider.svg";
import { ReactComponent as NotifIcon } from "icons/bell.svg";
import { ReactComponent as MetaIcon } from "icons/eye.svg";
import { ReactComponent as SchedulerIcon } from "icons/timer.svg";

const ToasterWrapper = styled.div`
  z-index: 100;
  top: 0;
  right: 0;
  padding: 32px 32px 0;
`;

const iconSet = {
  Crawler: SpiderIcon,
  Metadata: MetaIcon,
  Scheduler: SchedulerIcon,
};

const ToastNotif = (props) => {
  const [show, setShow] = useState(true);
  const title = props.title ? props.title : "Notification";
  const RenderedIcon = iconSet[props.title] ? iconSet[props.title] : NotifIcon;
  return (
    <Toast
      onClose={() => {
        setShow(false);
      }}
      show={show}
      delay={50000}
      autohide
    >
      <Toast.Header>
        <RenderedIcon
          style={{ width: "18px", height: "18px" }}
          className="mr-2"
        />
        <strong className="mr-auto">{title}</strong>
        <small>just now</small>
      </Toast.Header>
      <Toast.Body>{props.text}</Toast.Body>
    </Toast>
  );
};

const Toaster = (props) => {
  return (
    <ToasterWrapper
      aria-live="polite"
      aria-atomic="true"
      className="position-absolute"
    >
      {props.toastList.map((toast, idx) => {
        return <ToastNotif key={idx} title={toast.title} text={toast.text} />;
      })}
    </ToasterWrapper>
  );
};

export default Toaster;
