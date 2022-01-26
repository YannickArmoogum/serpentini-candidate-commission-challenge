"use strict";
import * as fs from "fs";

let rawdata = fs.readFileSync("./data/input.json");
let inputData = JSON.parse(rawdata);

function main() {
  let commissions = [];
  let deals = [];

  //Takes one user id and objective and loop through the list of deals to pick the right deals
  inputData.users.map((user) => {
    commissions.push(makeTransaction(user.id, user.objective).commissions);
    deals.push(makeTransaction(user.id, user.objective).deals);
  });

  deals = formatDeals(deals);

  let output = {
    commissions,
    deals,
  };

  let data = JSON.stringify(output);
  fs.writeFileSync("./data/output.json", data);
}

function makeTransaction(id, objective) {
  let dealsArray = [];

  inputData.deals.map((deal) => {
    if (id === deal.user) {
      let previousValidatedDeal = compareDates(deal.close_date, id);
      dealsArray.push({
        id: deal.id,
        commission: calculateCommissionPerTransaction(
          deal.amount,
          objective,
          previousValidatedDeal
        ),
        date: deal.payment_date.slice(0, 7),
      });
    }
  });

  let result = {};

  let commissions = {
    user_id: id,
    commission: calculateTotalCommissionPerMonth(dealsArray),
  };

  result = { commissions, deals: dealsArray };

  return result;
}

function compareDates(currentClosedDate, id) {
  //Check through array if there has been a sale with payment before the actual date
  let accumulatedDeals = inputData.deals.filter((deal) => {
    if (deal.user === id) {
      return deal.payment_date <= currentClosedDate;
    }
  });

  let total = 0;
  accumulatedDeals.forEach((deal) => {
    total += deal.amount;
  });

  return total;
}

function calculateCommissionPerTransaction(
  amount,
  objective,
  previousValidatedDeal
) {
  let totalCommisionAccumulated = 0;
  let halfObjective = objective / 2;

  if (previousValidatedDeal > 0) {
    totalCommisionAccumulated += takethirdSlice(amount);

    return totalCommisionAccumulated;
  }

  if (amount > halfObjective) {
    //Take 50% of the objective and continue to next slice
    totalCommisionAccumulated = takeFirstSlice(halfObjective);
    amount -= halfObjective;
    if (amount > objective) {
      amount -= halfObjective;
      totalCommisionAccumulated +=
        takeSecondSlice(halfObjective) + takethirdSlice(amount);
    } else {
      totalCommisionAccumulated += takeSecondSlice(amount);
    }
  } else {
    totalCommisionAccumulated = takeFirstSlice(amount);
  }

  return totalCommisionAccumulated;
}

function takeFirstSlice(amount) {
  let firstSliceAmt = amount * 0.05;
  return Number(firstSliceAmt.toFixed(1));
}

function takeSecondSlice(amount) {
  let secondSliceAmt = amount * 0.1;
  return Number(secondSliceAmt.toFixed(1));
}

function takethirdSlice(amount) {
  let thirdSliceAmt = amount * 0.15;
  return Number(thirdSliceAmt.toFixed(1));
}

function formatDeals(dealArray) {
  let tempArr = [];
  dealArray.map((deal) => {
    deal.map((innerDeals) => {
      tempArr.push({
        id: innerDeals.id,
        commission: Number(innerDeals.commission.toFixed(1)),
      });
    });
  });

  return tempArr;
}

function calculateTotalCommissionPerMonth(deals) {
  const deal = deals.reduce(
    (a, { date, commission }) => ((a[date] = (a[date] || 0) + +commission), a),
    {}
  );
  return deal;
}

main();
