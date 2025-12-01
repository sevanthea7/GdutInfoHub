// src/mock/mockWaterElectricData.d.ts
declare module "@/mock/mockWaterElectricData" {
  export interface WaterItem {
    title: string;
    url: string;
    date: string;
    content: string;
    key_words: string[];
    department: string;
  }

  export interface MockWaterElectricData {
    code: number;
    msg: string;
    data: {
      items: WaterItem[];
    };
  }

  export const mockNoticeData: MockWaterElectricData;
}
