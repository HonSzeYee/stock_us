# stock_us

一个用于美股交易记录的本地计算器（含 moomoo MY 手续费口径），支持均薄成本、已实现/未实现盈亏、ROI、导入导出与本地保存。

## 技术栈
- Vite + Vanilla JS
- flatpickr（日期选择器）
- localStorage（本地保存）

## 功能
- 交易流水录入（买入/卖出）
- 自动计算手续费与持仓均薄成本
- 已实现/未实现盈亏、总盈亏、ROI
- 累计手续费
- JSON 导入/导出
- 本地自动保存（localStorage）

## 运行
> 需要先安装 Node.js（LTS）。

1. 安装依赖
```powershell
npm install
```

2. 启动开发服务器
```powershell
npm run dev
```

浏览器访问：
```
http://localhost:5173/
```

## Windows 快捷启动
已提供脚本：
- `run-dev.bat`
- `run-dev-open.bat`（自动打开浏览器）

## 数据存储
- Key: `avg_cost_roi_moomoo_v1`
- 存放于浏览器的 localStorage

## 结构
- `index.html`
- `src/main.js`
- `src/style.css`

## 备注
- 手续费口径：逐项计费 → 单项四舍五入到 1 美分 → 求和
- 日期控件：flatpickr（带确认）

