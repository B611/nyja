import { Container, Row, Col, TabContainer, TabContent } from "react-bootstrap";
import { Menu, CrawlTab, DatabaseTab, StatsTab, Toaster } from "components";
import styled from "styled-components";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState, useEffect } from "react";
import { PopulateModal, SchedulerModal } from "components";

const AppContainer = styled(Container)`
  padding: 32px 0 0;
`;

const MenuContainer = styled(Container)``;

const PageContainer = styled(Container)``;

const MainPage = (props) => {
  const [toastList, setToastList] = useState([]);
  const [schedulerModalVisible, setSchedulerModalVisible] = useState(false);
  const [populateModalVisible, setPopulateModalVisible] = useState(
    !(localStorage.getItem("populated") === "true")
  );

  const showToast = (title, text) => {
    setToastList(toastList.concat({ title: title, text: text }));
  };

  useEffect(() => {
    const removeToast = () => {
      setToastList(toastList.slice(1));
    };
    const interval = setInterval(removeToast, 6000);
    return () => clearInterval(interval);
  }, [toastList]);

  return (
    <div style={{ position: "relative" }}>
      <Toaster toastList={toastList} />
      <AppContainer fluid>
        <Row xs={2}>
          <TabContainer
            defaultActiveKey={
              props.location.hash ? props.location.hash : "#crawl"
            }
          >
            <Col xs="auto">
              <MenuContainer fluid>
                <Row>
                  <Col>
                    <Menu />
                  </Col>
                </Row>
              </MenuContainer>
            </Col>
            <Col xs={8}>
              <PageContainer fluid>
                <Row>
                  <Col>
                    <TabContent>
                      <CrawlTab
                        toaster={showToast}
                        populateVisible={setPopulateModalVisible}
                        schedulerVisible={setSchedulerModalVisible}
                      />
                      <DatabaseTab toaster={showToast} />
                      <StatsTab />
                    </TabContent>
                  </Col>
                </Row>
              </PageContainer>
            </Col>
          </TabContainer>
        </Row>
      </AppContainer>
      <PopulateModal
        populateModalVisible={populateModalVisible}
        setPopulateModalVisible={setPopulateModalVisible}
        showToast={showToast}
      />
      <SchedulerModal
        visible={schedulerModalVisible}
        setVisible={setSchedulerModalVisible}
        showToast={showToast}
      />
    </div>
  );
};

export default MainPage;
