import { writable } from 'svelte/store';

// Initial data
let initialData = {
  ut: "ut1XXX",
  name: "Business Manager",
  time_status: "Unfilled",
  traders: [
    {
      ut: "ut11XX",
      name: "Trader1",
      entity: "CA-CIB Paris",
      status: "Unfilled",
      product_line: "Rate Non Linear",
      cdrs: [
        { id: 11, name: "XXXXX", times: [0.8, 0.2, 0.5, 1, 0, 0, 1, 0.7, 1, 1, 0, 0] },
        { id: 12, name: "LOCAL", times: [0.2, 0.8, 0.5, 0, 1, 1, 0, 0.3, 0, 0, 1, 0] },
      ],
    },
    {
      ut: "ut22XX",
      name: "Trader2",
      entity: "CA-CIB New York",
      status: "Unfilled",
      product_line: "Primary Credit",
      cdrs: [
        { id: 21, name: "XXXXX", times: [0.6, 0.1, 0.2, 0.3, 0.1, 0, 0.9, 0.2, 0.2, 0.2, 0.4, 0] },
        { id: 22, name: "YYYYY", times: [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0] },
        { id: 23, name: "LOCAL", times: [0.3, 0.8, 0.7, 0.6, 0.8, 0.9, 0, 0.7, 0.7, 0.7, 0.5, 0] },
      ],
    },
    {
      ut: "ut33XX",
      name: "Trader3",
      entity: "CA-CIB London",
      status: "Unfilled",
      product_line: "Forex linear",
      cdrs: [
        { id: 31, name: "XXXXX", times: [0.1, 0.8, 0.2, 0.1, 0.1, 0.5, 0.6, 0.6, 0.5, 0.1, 0.5, 0] },
        { id: 32, name: "YYYYY", times: [0.9, 0.2, 0.8, 0.9, 0.9, 0.5, 0.4, 0.4, 0.5, 0.9, 0.5, 0]},
      ],
    },
  ],
};

// Create a writable store with the initial data
export const businessManagerStore = writable(initialData);
