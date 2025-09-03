# Budget Control & EVM — Project Alpha

Data date: 2025-08-27
Currency: THB

Columns:
- WBS, TaskID, TaskName, BAC_THB, PlannedPctToDate, PercentComplete
- EV_THB, PV_THB, AC_ToDate_THB, CV_THB, SV_THB, CPI, SPI, Status

| WBS | TaskID | TaskName                | BAC_THB  | PlannedPctToDate | PercentComplete | EV_THB  | PV_THB  | AC_ToDate_THB | CV_THB  | SV_THB  | CPI    | SPI  | Status                    |
|-----|--------|-------------------------|----------|------------------|-----------------|---------|---------|----------------|---------|---------|--------|------|---------------------------|
| 1.0 | T001   | Project Initiation      | 200,000  | 1.00             | 1.00            | 200,000 | 200,000 | 210,000        | -10,000 | 0       | 0.9524 | 1.00 | Over Budget               |
| 1.1 | T002   | Design & Permitting     | 800,000  | 1.00             | 0.80            | 640,000 | 800,000 | 820,000        | -180,000| -160,000| 0.7805 | 0.80 | At Risk (Cost & Schedule) |
| 2.0 | T003   | Site Preparation        | 500,000  | 1.00             | 0.60            | 300,000 | 500,000 | 450,000        | -150,000| -200,000| 0.6667 | 0.60 | At Risk (Cost & Schedule) |
| 3.0 | T004   | Foundation              |1,500,000 | 0.50             | 0.30            | 450,000 | 750,000 | 400,000        | 50,000  | -300,000| 1.1250 | 0.60 | Behind Schedule           |
| 4.0 | T005   | Structure - Ground Flr  |2,000,000 | 0.00             | 0.00            | -       | -       | 0              | -       | -       | -      | -    | Not Started               |
| 4.1 | T006   | Structure - Upper Flrs  |3,000,000 | 0.00             | 0.00            | -       | -       | 0              | -       | -       | -      | -    | Not Started               |
| 5.0 | T007   | MEP Rough-in            |1,200,000 | 0.00             | 0.00            | -       | -       | 0              | -       | -       | -      | -    | Not Started               |
| 6.0 | T008   | Enclosure (Façade/Roof) |1,400,000 | 0.00             | 0.00            | -       | -       | 0              | -       | -       | -      | -    | Not Started               |
| 7.0 | T009   | Interior Fit-out        |2,200,000 | 0.00             | 0.00            | -       | -       | 0              | -       | -       | -      | -    | Not Started               |
| 8.0 | T010   | Testing & Commissioning | 300,000  | 0.00             | 0.00            | -       | -       | 0              | -       | -       | -      | -    | Not Started               |

Totals (Active Work):
- EV ≈ 1,590,000; AC ≈ 1,880,000; PV ≈ 2,250,000
- CPI ≈ 0.85; SPI ≈ 0.71

Formulas (อ้างอิงหากต้องคำนวณเพิ่ม):
- CV = EV − AC
- SV = EV − PV
- CPI = EV / AC
- SPI = EV / PV
- EAC แนวทางทั่วไป:
  - EAC₁ = AC + (BAC − EV)
  - EAC₂ = BAC / CPI
  - EAC₃ = AC + (BAC − EV) / (CPI × SPI)
- ETC = EAC − AC
- TCPI = (BAC − EV) / (BAC − AC) หรือ (BAC − EV) / (EAC − AC)