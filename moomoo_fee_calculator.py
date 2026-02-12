from decimal import Decimal, ROUND_HALF_UP


def _round2(x):
    # 使用“商业四舍五入”，避免 Python round 的银行家舍入
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def moomoo_fee_usd(price, shares, myr_to_usd=0.25346, verbose=False):
    """
    moomoo MY 美股正股交易费用计算器（纯美元版）

    输入：
    price  : 股票价格（USD）
    shares : 股数

    输出：
    买入费用、卖出费用、一轮T总费用、每股成本
    """

    # 成交金额
    amount = price * shares

    # 1）佣金：0.03% * 成交金额（最低 $0.01）-（当前免佣金）
    commission = 0

    # 2）平台使用费：每笔订单固定 $0.99
    platform_fee = 0.99

    # 3）交收费：$0.003/股（最高不超过成交金额的 1%），单项进位/四舍五入到美分
    clearing_fee_raw = min(shares * 0.003, amount * 0.01)
    clearing_fee = _round2(clearing_fee_raw)

    # 4）交易活动费 TAF：仅卖出收取（最低 $0.01，最高 $9.79），单项进位/四舍五入到美分
    taf_fee_raw = min(max(shares * 0.000195, 0.01), 9.79)
    taf_fee = _round2(taf_fee_raw)

    # 5）印花税（马来西亚）：每 RM1,000 或部分收 RM1，单笔最高 RM1,000
    amount_myr = amount / myr_to_usd
    if amount_myr > 0:
        stamp_duty_myr = min((int((amount_myr - 1) // 1000) + 1) * 1, 1000)
    else:
        stamp_duty_myr = 0
    # 印花税换算到 USD 后，按美分进位/四舍五入
    stamp_duty_usd_raw = stamp_duty_myr * myr_to_usd
    stamp_duty_usd = _round2(stamp_duty_usd_raw)

    # 买入总费用（含印花税）
    buy_fee = commission + platform_fee + clearing_fee + stamp_duty_usd

    # 卖出总费用（多一个 TAF + 印花税）
    sell_fee = commission + platform_fee + clearing_fee + taf_fee + stamp_duty_usd

    # 做一轮T总费用（买+卖）
    round_trip_fee = buy_fee + sell_fee

    # 每股成本
    cost_per_share = round_trip_fee / shares

    # App 展示通常保留 2 位小数，这里统一四舍五入显示
    if verbose:
        breakdown = {
            "成交金额(USD)": amount,
            "佣金(USD)": commission,
            "平台使用费(USD)": platform_fee,
            "交收费(USD)": clearing_fee,
            "交易活动费TAF(USD)": taf_fee,
            "印花税(MYR)": stamp_duty_myr,
            "印花税(USD)": stamp_duty_usd,
            "买入费用(USD)": buy_fee,
            "卖出费用(USD)": sell_fee,
            "做一轮T总费用(USD)": round_trip_fee,
            "每股成本(USD)": cost_per_share
        }

        print("\n====== 费用明细（单项进位后） ======")
        for k, v in breakdown.items():
            if "MYR" in k:
                print(f"{k}: {v:.4f}")
            else:
                print(f"{k}: {v:.6f}")

    # App 展示通常保留 2 位小数，这里统一四舍五入显示
    return {
        "买入费用(USD)": round(buy_fee, 2),
        "卖出费用(USD)": round(sell_fee, 2),
        "做一轮T总费用(USD)": round(round_trip_fee, 2),
        "每股成本(USD)": round(cost_per_share, 2)
    }


# ==========================
# 运行输入
# ==========================
if __name__ == "__main__":
    price = float(input("请输入股票价格（USD）："))
    shares = int(input("请输入股数："))
    fx = input("请输入 1 MYR 兑换 USD 的汇率（默认 0.25346）：").strip()
    myr_to_usd = float(fx) if fx else 0.25346

    result = moomoo_fee_usd(price, shares, myr_to_usd=myr_to_usd, verbose=True)

    print("\n====== moomoo MY 手续费计算结果（纯USD） ======")
    for k, v in result.items():
        print(f"{k}: {v:.4f}")
