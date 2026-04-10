"use client";

import { Pagination as BsPagination } from "react-bootstrap";

type Props = {
  page: number;
  total: number;
  pageSize: number;
  onPageChange: (page: number) => void;
};

export function Pagination({ page, total, pageSize, onPageChange }: Props) {
  const totalPages = Math.ceil(total / pageSize);
  if (totalPages <= 1) return null;

  return (
    <BsPagination className="mb-0 mt-3 justify-content-end">
      <BsPagination.Prev disabled={page === 1} onClick={() => onPageChange(page - 1)} />
      {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
        <BsPagination.Item key={p} active={p === page} onClick={() => onPageChange(p)}>
          {p}
        </BsPagination.Item>
      ))}
      <BsPagination.Next disabled={page === totalPages} onClick={() => onPageChange(page + 1)} />
    </BsPagination>
  );
}
