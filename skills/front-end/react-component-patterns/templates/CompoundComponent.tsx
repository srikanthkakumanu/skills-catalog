// Drop-in compound-component starter (context + parent + children) for a Tabs- or
// Accordion-shaped problem. Rename Tabs/TabsTrigger/TabsPanel to fit the actual component.
'use client';

import { createContext, useContext, useState } from 'react';

type TabsContextValue = {
  activeTab: string;
  setActiveTab: (id: string) => void;
};

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabsContext(): TabsContextValue {
  const ctx = useContext(TabsContext);
  if (!ctx) {
    throw new Error('Tabs.Trigger and Tabs.Panel must be rendered inside <Tabs>');
  }
  return ctx;
}

type TabsProps = {
  defaultTab: string;
  children: React.ReactNode;
};

export function Tabs({ defaultTab, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div role="tablist">{children}</div>
    </TabsContext.Provider>
  );
}

type TabsTriggerProps = {
  id: string;
  children: React.ReactNode;
};

Tabs.Trigger = function TabsTrigger({ id, children }: TabsTriggerProps) {
  const { activeTab, setActiveTab } = useTabsContext();
  const selected = activeTab === id;
  return (
    <button type="button" role="tab" aria-selected={selected} onClick={() => setActiveTab(id)}>
      {children}
    </button>
  );
};

type TabsPanelProps = {
  id: string;
  children: React.ReactNode;
};

Tabs.Panel = function TabsPanel({ id, children }: TabsPanelProps) {
  const { activeTab } = useTabsContext();
  if (activeTab !== id) return null;
  return <div role="tabpanel">{children}</div>;
};
