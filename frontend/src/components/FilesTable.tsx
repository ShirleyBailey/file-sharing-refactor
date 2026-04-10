"use client";

import { Badge, Button, Spinner, Table } from "react-bootstrap";
import { FileItem, getDownloadUrl } from "@/lib/api";
import { formatDate, formatSize, getProcessingVariant } from "@/lib/format";

type Props = {
  items: FileItem[];
  isLoading: boolean;
};

export function FilesTable({ items, isLoading }: Props) {
  if (isLoading) {
    return (
      <div className="d-flex justify-content-center py-5">
        <Spinner animation="border" />
      </div>
    );
  }

  return (
    <div className="table-responsive">
      <Table hover bordered className="align-middle mb-0">
        <thead className="table-light">
          <tr>
            <th>Название</th>
            <th>Файл</th>
            <th>MIME</th>
            <th>Размер</th>
            <th>Статус</th>
            <th>Проверка</th>
            <th>Создан</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {items.length === 0 ? (
            <tr>
              <td colSpan={8} className="text-center py-4 text-secondary">
                Файлы пока не загружены
              </td>
            </tr>
          ) : (
            items.map((file) => (
              <tr key={file.id}>
                <td>
                  <div className="fw-semibold">{file.title}</div>
                  <div className="small text-secondary">{file.id}</div>
                </td>
                <td>{file.original_name}</td>
                <td>{file.mime_type}</td>
                <td>{formatSize(file.size)}</td>
                <td>
                  <Badge bg={getProcessingVariant(file.processing_status)}>
                    {file.processing_status}
                  </Badge>
                </td>
                <td>
                  <div className="d-flex flex-column gap-1">
                    <Badge bg={file.requires_attention ? "warning" : "success"}>
                      {file.scan_status ?? "pending"}
                    </Badge>
                    <span className="small text-secondary">
                      {file.scan_details ?? "Ожидает обработки"}
                    </span>
                  </div>
                </td>
                <td>{formatDate(file.created_at)}</td>
                <td className="text-nowrap">
                  <Button
                    as="a"
                    href={getDownloadUrl(file.id)}
                    variant="outline-primary"
                    size="sm"
                  >
                    Скачать
                  </Button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    </div>
  );
}
