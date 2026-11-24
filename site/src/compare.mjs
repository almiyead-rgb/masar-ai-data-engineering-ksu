/** Compare student-exported metrics locally. Never execute or upload file content. */
export function compareMetrics(observed, reference) {
  const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
  if (!object(reference) || !object(reference.metrics)) throw new Error('Invalid reference contract');
  if (!object(observed)) return {status:'invalid',issues:['The JSON file must contain an object.'],checks:[],extras:[]};
  const issues=[];
  for (const key of ['schema_version','day','dataset']) {
    if (!Object.hasOwn(observed,key)) issues.push(`Missing required field: ${key}.`);
    else if (observed[key] !== reference[key]) issues.push(`${key} must be ${JSON.stringify(reference[key])}; received ${JSON.stringify(observed[key])}.`);
  }
  if (!object(observed.metrics)) issues.push('metrics must be a JSON object.');
  if (issues.length) return {status:'invalid',issues,checks:[],extras:[]};
  const checks=[],extras=[];
  function visit(expected,actual,path,present=true) {
    if (object(expected)) {
      if (!object(actual)) {checks.push({path,expected,observed:actual,present,match:false});return;}
      for (const key of Object.keys(expected)) visit(expected[key],actual[key],`${path}.${key}`,Object.hasOwn(actual,key));
      for (const key of Object.keys(actual)) if (!Object.hasOwn(expected,key)) extras.push(`${path}.${key}`);
    } else if (Array.isArray(expected)) {
      checks.push({path,expected,observed:actual,present,match:present&&Array.isArray(actual)&&actual.length===expected.length&&expected.every((v,i)=>typeof v===typeof actual[i]&&JSON.stringify(v)===JSON.stringify(actual[i]))});
    } else {
      checks.push({path,expected,observed:actual,present,match:present&&typeof expected===typeof actual&&actual===expected});
    }
  }
  visit(reference.metrics,observed.metrics,'metrics');
  for(const key of Object.keys(observed)) if(!['schema_version','day','dataset','metrics'].includes(key)) extras.push(key);
  return {status:checks.every(c=>c.match)?'match':'mismatch',issues,checks,extras};
}
