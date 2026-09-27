export const formatPercentage = (decimal: number): string => {
  return `${Math.round(decimal * 100)}%`;
};

export const formatDuration = (hours: number): string => {
  if (hours < 1) {
    return `${Math.round(hours * 60)} mins`;
  }
  return `${hours.toFixed(1)} hrs`;
};
