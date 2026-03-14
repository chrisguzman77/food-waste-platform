export function formatDateTime(value: string): string {
  return new Date(value).toLocaleString();
}

export function formatQuantity(quantity: number, unit: string): string {
  return `${quantity} ${unit}`;
}