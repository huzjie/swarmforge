import React from 'react';

interface AgentCardProps {
  className?: string;
}

export const AgentCard: React.FC<AgentCardProps> = ({ className }) => {
  return <div className={className}>{/* AgentCard component */}</div>;
};
