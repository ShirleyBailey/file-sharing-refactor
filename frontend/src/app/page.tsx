"use client";

import { useCallback, useState } from "react";
import { Alert, Badge, Button, Card, Col, Container, Row } from "react-bootstrap";
import { fetchAlerts, fetchFiles } from "@/lib/api";
import { AlertsTable } from "@/components/AlertsTable";
import { FilesTable } from "@/components/FilesTable";
import { Pagination } from "@/components/Pagination";
import { UploadModal } from "@/components/UploadModal";
import { usePaginatedData } from "@/hooks/usePaginatedData";

const PAGE_SIZE = 20;

export default function Page() {
  const [showModal, setShowModal] = useState(false);

  const fetchFilesFn = useCallback(
    (page: number, pageSize: number) => fetchFiles(page, pageSize),
    [],
  );
  const fetchAlertsFn = useCallback(
    (page: number, pageSize: number) => fetchAlerts(page, pageSize),
    [],
  );

  const files = usePaginatedData(fetchFilesFn, PAGE_SIZE);
  const alerts = usePaginatedData(fetchAlertsFn, PAGE_SIZE);

  const errorMessage = files.error ?? alerts.error;

  function handleRefresh() {
    void files.load(files.page);
    void alerts.load(alerts.page);
  }

  function handleUploaded() {
    void files.load(1);
  }

  return (
    <Container fluid className="py-4 px-4 bg-light min-vh-100">
      <Row className="justify-content-center">
        <Col xxl={10} xl={11}>
          <Card className="shadow-sm border-0 mb-4">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start gap-3 flex-wrap">
                <div>
                  <h1 className="h3 mb-2">Управление файлами</h1>
                  <p className="text-secondary mb-0">
                    Загрузка файлов, просмотр статусов обработки и ленты алертов.
                  </p>
                </div>
                <div className="d-flex gap-2">
                  <Button variant="outline-secondary" onClick={handleRefresh}>
                    Обновить
                  </Button>
                  <Button variant="primary" onClick={() => setShowModal(true)}>
                    Добавить файл
                  </Button>
                </div>
              </div>
            </Card.Body>
          </Card>

          {errorMessage && (
            <Alert variant="danger" className="shadow-sm">
              {errorMessage}
            </Alert>
          )}

          <Card className="shadow-sm border-0 mb-4">
            <Card.Header className="bg-white border-0 pt-4 px-4">
              <div className="d-flex justify-content-between align-items-center">
                <h2 className="h5 mb-0">Файлы</h2>
                <Badge bg="secondary">{files.data?.total ?? 0}</Badge>
              </div>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
              <FilesTable items={files.data?.items ?? []} isLoading={files.isLoading} />
              {files.data && (
                <Pagination
                  page={files.page}
                  total={files.data.total}
                  pageSize={PAGE_SIZE}
                  onPageChange={(p) => void files.load(p)}
                />
              )}
            </Card.Body>
          </Card>

          <Card className="shadow-sm border-0">
            <Card.Header className="bg-white border-0 pt-4 px-4">
              <div className="d-flex justify-content-between align-items-center">
                <h2 className="h5 mb-0">Алерты</h2>
                <Badge bg="secondary">{alerts.data?.total ?? 0}</Badge>
              </div>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
              <AlertsTable items={alerts.data?.items ?? []} isLoading={alerts.isLoading} />
              {alerts.data && (
                <Pagination
                  page={alerts.page}
                  total={alerts.data.total}
                  pageSize={PAGE_SIZE}
                  onPageChange={(p) => void alerts.load(p)}
                />
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <UploadModal
        show={showModal}
        onHide={() => setShowModal(false)}
        onUploaded={handleUploaded}
      />
    </Container>
  );
}
